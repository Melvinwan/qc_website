from staticfiles.RFSoC_controller import RFSoC_controller
from staticfiles.Toptica_ophyd import LaserToptica
from staticfiles.caylar_magnet_ophyd import CaylarMagnet
from staticfiles.ITC_ophyd import MercuryITCDevice
from staticfiles.XMLGenerator import xml_config_to_dict

def construct_object():
    rfsoc_host = xml_config_to_dict("staticfiles/xilinx_host.xml")
    caylar_host = xml_config_to_dict("staticfiles/caylar.xml")
    itc_host = xml_config_to_dict("staticfiles/mercuryITC.xml")
    toptica_host = xml_config_to_dict("staticfiles/toptica.xml")
    LTDLC = LaserToptica(prefix="...",name="LTDLC",config_host=toptica_host)
    RFSoC = RFSoC_controller(config_host=rfsoc_host)
    magneticIR = CaylarMagnet("H", name="magneticIR",config_host=caylar_host)
    ITCD = MercuryITCDevice(prefix="...",name="ITCD", host="itc-optistat.psi.ch",config_host=itc_host)
    return RFSoC, LTDLC, magneticIR, ITCD

def construct_toptica():
    toptica_host = xml_config_to_dict("staticfiles/toptica.xml")
    LTDLC = LaserToptica(prefix="...",name="LTDLC",config_host=toptica_host)
    # LTDLC.try_connect()
    return LTDLC

def construct_rfsoc():
    rfsoc_host = xml_config_to_dict("staticfiles/xilinx_host.xml")
    RFSoC = RFSoC_controller(config_host=rfsoc_host)
    # RFSoC.try_connect()
    return RFSoC

def construct_caylar():
    caylar_host = xml_config_to_dict("staticfiles/caylar.xml")
    magneticIR = CaylarMagnet("H", name="magneticIR",config_host=caylar_host)
    # magneticIR.try_connect()
    return magneticIR

def construct_itc():
    itc_host = xml_config_to_dict("staticfiles/mercuryITC.xml")
    ITCD = MercuryITCDevice(prefix="...",name="ITCD", host="itc-optistat.psi.ch",config_host=itc_host)
    # ITCD.try_connect()
    return ITCD