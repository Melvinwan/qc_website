import functools
import threading
import time
from typing import List
import abc
import typing
import logging
from ophyd.log import config_ophyd_logging
# config_ophyd_logging(file='/tmp/ophyd.log', level='DEBUG')
from prettytable import PrettyTable
from .log_ophyd import log_ophyd

import numpy as np
# from bec_utils import BECMessage, MessageEndpoints, bec_logger
from ophyd import Component as Cpt
from ophyd import Device, PositionerBase, Signal
from ophyd.status import wait as status_wait
from ophyd.utils import LimitError, ReadOnlyError

from ophyd.ophydobj import OphydObject

# import asyncio
from IPython.display import clear_output
from mercuryitc import MercuryITC

logger = log_ophyd("ITC_log.txt",__name__)

DEFAULT_EPICSSIGNAL_VALUE = object()
class ITCCommunicationError(Exception):
    pass


class ITCError(Exception):
    pass


# def retry_once(fcn):
#     """Decorator to rerun a function in case a ITC communication error was raised. This may happen if the buffer was not empty."""

#     @functools.wraps(fcn)
#     def wrapper(self, *args, **kwargs):
#         try:
#             val = fcn(self, *args, **kwargs)
#         except (ITCCommunicationError, ITCError):
#             val = fcn(self, *args, **kwargs)
#         return val

#     return wrapper

# def threadlocked(fcn):
#     """Ensure that the thread acquires and releases the lock."""

#     @functools.wraps(fcn)
#     def wrapper(self, *args, **kwargs):
#         lock = self._lock if hasattr(self, "_lock") else self.ITC._lock
#         with lock:
#             return fcn(self, *args, **kwargs)

#     return wrapper

_type_map = {
    "number": (float, np.floating),
    "array": (np.ndarray, list, tuple),
    "string": (str,),
    "integer": (int, np.integer),
}

def data_shape(val):
    """Determine data-shape (dimensions)

    Returns
    -------
    list
        Empty list if val is number or string, otherwise
        ``list(np.ndarray.shape)``
    """
    if data_type(val) != "array":
        return []

    try:
        return list(val.shape)
    except AttributeError:
        return [len(val)]


def data_type(val):
    """Determine the JSON-friendly type name given a value

    Returns
    -------
    str
        One of {'number', 'integer', 'array', 'string'}

    Raises
    ------
    ValueError if the type is not recognized
    """
    bad_iterables = (str, bytes, dict)
    if isinstance(val, typing.Iterable) and not isinstance(val, bad_iterables):
        return "array"

    for json_type, py_types in _type_map.items():
        if isinstance(val, py_types):
            return json_type

    raise ValueError(
        f"Cannot determine the appropriate bluesky-friendly data type for "
        f"value {val} of Python type {type(val)}. "
        f"Supported types include: int, float, str, and iterables such as "
        f"list, tuple, np.ndarray, and so on."
    )

class ITCController(OphydObject): #On off laser similar to controller
    _controller_instances = {}
    SUB_CONNECTION_CHANGE = "connection_change"

    def __init__(
        self,
        *,
        name=None,
        host=None,
        port=None,
        attr_name="",
        parent=None,
        labels=None,
        kind=None,
    ):
        if not hasattr(self, "_initialized"):
            super().__init__(
                name=name, attr_name=attr_name, parent=parent, labels=labels, kind=kind
            )

            self._lock = threading.RLock()
            self.host = host
            self.port = port
            self._initialized = True
            # self._initialize()

    def _initialize(self):
        # self._connected = False
        # print(f"connecting to {self.host}")
        # logger.info("The connection has already been established.")
        # try:
        #     self.connect()

        # except Exception as err:
        #     print("Connection cannot be established please retry")
        # self._set_default_values()
        self.name = "MercuryITC"
        # self.is_open = True

    # def _set_default_values(self):
    #     # no. of axes controlled by each controller
    #     self._wavelength_act = 1550

    @property
    def connected(self):
        """
        The function returns the value of the "_connected" attribute.
        @returns The method is returning the value of the variable `_connected`.
        """
        return self._connected

    def connect(self):
        """
        The function connects to a Mercury ITC device and returns True if the connection is successful,
        otherwise it returns False.
        @returns The connect() method returns a boolean value. If the connection to the Mercury ITC is
        successful, it returns True. If the connection fails, it returns False.
        """
        print("connecting to Mercury ITC")
        try:

            self.ITC = MercuryITC(f"TCPIP0::{self.host}::{self.port}::SOCKET")
            self.htr = self.ITC.modules[1] #main htr
            self.temp = self.ITC.modules[2]
            self.aux = self.ITC.modules[0]
            self._connected = True
            print("Mercury ITC has been connected")
            return True
        except Exception as err:
            print("Mercury ITC cannot be connected")
            self._connected = False
            return False
    # def open(self):
    #     self.connect()
    #     self.is_open = True


    def off(self):
        """
        The function "off" closes the connection to the laser and updates the connection status.
        """
        """Close the connection to the laser"""
        logger.info("The connection is already closed.")
        self.ITC.disconnect()
        self.connected = False

    def get_itc_data(self):
        """
        The function `get_laser_data` returns a dictionary of various laser data values.
        @returns a dictionary called "signals" which contains various laser data values.
        """
        signals = {
            # "wide scan amplitude":{"value": self.ITC.laser1.wide_scan.amplitude.get()},
            # "wide scan offset":{"value": self.ITC.laser1.wide_scan.offset.get()},
            # "wide scan remaining time":{"value": self.ITC.laser1.wide_scan.remaining_time.get()},
            "Main heater volt":{"value": self.htr.volt},
            "Main heater current RO":{"value": self.htr.curr},
            "Main heater power":{"value": self.heater_power},#
            "Main heater voltage limit":{"value": self.htr.vlim},
            "Temperature sensor volt RO":{"value": self.temp.volt},
            "Temperature sensor excitation magnitude":{"value": self.temp.exct_mag},
            "Temperature sensor scaling factor":{"value": self.temp.cal_scal},
            "Temperature sensor offset":{"value": self.temp.cal_offs},
            "Temperature sensor hot limit":{"value": self.temp.cal_hotl},
            "Temperature sensor cold limit":{"value": self.temp.cal_coldl},
            "Temperature sensor temperature":{"value": self.temp.temp},#
            "Temperature sensor sensitivity":{"value": self.temp.slop},
            "Temperature sensor associate heater":{"value": self.temp.loop_temp},
            "Temperature sensor associate auxiliary":{"value": self.temp.loop_aux},
            "Temperature sensor propotional gain":{"value": self.temp.loop_p},
            "Temperature sensor internal gain":{"value": self.temp.loop_i},
            "Temperature sensor differential gain":{"value": self.temp.loop_d},
            "Temperature sensor Enables or disables automatic gas flow":{"value": self.temp.loop_faut},
            "Temperature sensor ramp speed in K/min":{"value": self.temp.loop_rset},
            "Temperature sensor Enables or disables temperature ramp":{"value": self.temp.loop_rena},
            "Gas flow minimum flow":{"value": self.aux.gmin},
            "Gas flow Temperature error sensitivity":{"value": self.aux.tes},
            "Gas flow Temperature voltage error sensitivity":{"value": self.aux.tves},
            "Gas flow stepper speed":{"value": self.aux.spd},
            "Gas flow position stepper motor":{"value": self.aux.step},


        }
        return signals

    def heater_power(self):
        logger.debug(f"recv heater power")
        return self.htr.powr

    def heater_power_setter(self,val):
        logger.debug(f"set scan end")
        self.htr.powr = val
    def temperature(self):
        logger.debug(f"recv temperature")
        return self.temp.temp[0]

    def temperature_setter(self,val):
        logger.debug(f"set temperature")
        self.temp.temp = val

    def describe(self) -> None:
        t = PrettyTable()
        t.title = f"{self.__class__.__name__} on {self.sock.host}:{self.sock.port}"
        t.field_names = [
            "heater power",
            "temperature"
        ]
        t.add_row(
                    [
                        self.heater_power(),
                        self.temperature(),
                    ]
                )
        print(t)

    # def __new__(cls, *args, **kwargs):
    #     socket = kwargs.get("socket")
    #     if not hasattr(socket, "host"):
    #         raise RuntimeError("Socket must specify a host.")
    #     if not hasattr(socket, "port"):
    #         raise RuntimeError("Socket must specify a port.")
    #     host_port = f"{socket.host}:{socket.port}"
    #     if host_port not in Controller._controller_instances:
    #         Controller._controller_instances[host_port] = object.__new__(cls)
    #     return Controller._controller_instances[host_port]
class ITCSignalBase(abc.ABC,Signal): #Similar to socketsignal
    SUB_SETPOINT = "setpoint"
    def __init__(self, signal_name, **kwargs):
        self.signal_name = signal_name
        super().__init__(**kwargs)
        self.ITC = self.parent.itccontroller

    @abc.abstractmethod
    def _get(self):
        ...

    @abc.abstractmethod
    def _set(self, val):
        ...

    def get(self):
        self._readback = self._get()
        return self._readback

    def put(self, value):
        """Set the motor instance for a specified controller axis."""
        self._set(value)
        timestamp = time.time()
        old_value = self.get()
        VALUE = value
        super().put(value, timestamp=timestamp,force=True)
        self._run_subs(sub_type=self.SUB_SETPOINT, old_value=old_value,
                       value=VALUE, timestamp=self.timestamp)
    def describe(self):
        if self._readback is DEFAULT_EPICSSIGNAL_VALUE:
            val = self.get()
        else:
            val = self._readback
        return {
            self.name: {
                "source":self.ITC.name,
                "dtype": data_type(val),
                "shape":data_shape(val)
            }
        }

    # def get_laser(self, item):
    #     """Get motor instance for a specified controller axis."""
    #     return self._client.get(item)

class ITCSignalRO(ITCSignalBase):
    def __init__(self, signal_name, **kwargs):
        super().__init__(signal_name, **kwargs)
        self._metadata["write_access"] = False

    # @threadlocked
    def _set(self):
        raise ReadOnlyError("Read-only signals cannot be set")

class ITCHeaterPower(ITCSignalBase):
    # @threadlocked
    def _get(self):
        return self.ITC.heater_power()

    # @threadlocked
    def _set(self, val):
        logger.info("Heater power is set to "+str(val))
        self.ITC.heater_power_setter(val)

class ITCTemperature(ITCSignalBase):
    # @threadlocked
    def _get(self):
        return self.ITC.temperature()

    # @threadlocked
    def _set(self, val):
        logger.info("Temperature is set to "+str(val))
        self.ITC.temperature(val)

class MercuryITCDevice(Device):
    heater_power = Cpt(ITCHeaterPower, signal_name="heater_power",kind="hinted")
    temperature = Cpt(ITCTemperature, signal_name="temperature", kind="hinted")

    def __init__(self, prefix,name, host, port=None, kind=None,configuration_attrs=None, parent=None,config_host=None,**kwargs):
        if config_host==None:
            self.itccontroller = ITCController(host=host,port=port)
        else:
            self.itccontroller = ITCController(host=config_host["host"],port=config_host["port"])
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            # read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.name = name
        self.tolerance = kwargs.pop("tolerance", 0.5)
    def try_connect(self):
        return self.itccontroller.connect()
    def update_all_xml(self, xml):
        """
        The function updates the configuration settings of an ITC (Integrated Temperature Controller)
        using an XML file.
        @param xml - The `xml` parameter is a string that represents the XML content. It is used as
        input to update the configuration settings of the object.
        """
        from .XMLGenerator import xml_config_to_dict
        try:
            self.config = xml_config_to_dict(xml)
            self.update_heater_power(self.config["heater_power"])
            self.update_temperature(self.config["ITC_temperature"])
            print("ITC Updated")
        except:
            print("XML not Found")
    def update_heater_power(self,val):
        """
        The function updates the power of a heater in an ITC controller.
        @param val - The parameter "val" is the value that you want to set for the heater power.
        """
        self.itccontroller.heater_power_setter(val)
    def update_temperature(self,val):
        """
        The function updates the temperature value in the ITC controller.
        @param val - The parameter "val" is the new temperature value that you want to set.
        """
        self.itccontroller.temperature_setter(val)
    def report_heater_power(self):
        """
        The function returns the value of the heater power.
        @returns The value of the `heater_power` attribute.
        """
        return self.heater_power.get()
    def report_temperature(self):
        """
        The function returns the value of the scan_start attribute.
        @returns The value of `self.scan_start.get()` is being returned.
        """
        return self.temperature.get()

    def stage(self) -> List[object]:
        """
        The function returns the result of calling the `stage()` method of the superclass.
        @returns The method is returning a list of objects.
        """
        return super().stage()

    def unstage(self) -> List[object]:
        return super().unstage()

    def stop(self, *, success=False):
        self.controller.stop_all_axes()
        return super().stop(success=success)


if __name__ == "__main__":
    ITCD = MercuryITCDevice(prefix="...",name="ITCD", host="itc-optistat.psi.ch")
    ITCD.stage()
    print(ITCD.read())

    # print(ITCD.get())
    # print(ITCD.describe())

    ITCD.unstage()
