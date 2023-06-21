from staticfiles.RFSoC_controller import RFSoC_controller
from staticfiles.Toptica_ophyd import LaserToptica
from staticfiles.caylar_magnet_ophyd import CaylarMagnet
from staticfiles.ITC_ophyd import MercuryITCDevice
from staticfiles.XMLGenerator import xml_config_to_dict

def construct_object():
    rfsoc_host = xml_config_to_dict("staticfiles/xilinx_host.xml")["database"]
    caylar_host = xml_config_to_dict("staticfiles/caylar.xml")["database"]
    itc_host = xml_config_to_dict("staticfiles/mercuryITC.xml")["database"]
    toptica_host = xml_config_to_dict("staticfiles/toptica.xml")["database"]
    RFSoC = RFSoC_controller(config_host=rfsoc_host)
    LTDLC = LaserToptica(prefix="...",name="LTDLC", host="129.129.98.110", config_host=toptica_host)
    magneticIR = CaylarMagnet("H", name="magneticIR",config_host=caylar_host)
    ITCD = MercuryITCDevice(prefix="...",name="ITCD", host="itc-optistat.psi.ch",config_host=itc_host)
    return RFSoC, LTDLC, magneticIR, ITCD