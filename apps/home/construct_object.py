from staticfiles.RFSoC_controller import RFSoC_controller
from staticfiles.Toptica_ophyd import LaserToptica
from staticfiles.magnetic_Ophyd import Magnetic
from staticfiles.ITC_ophyd import MercuryITCDevice

def construct_object():
    RFSoC = RFSoC_controller()
    LTDLC = LaserToptica(prefix="...",name="LTDLC", host="129.129.98.110")
    magneticIR = Magnetic("H", name="magneticIR")
    ITCD = MercuryITCDevice(prefix="...",name="ITCD", host="itc-optistat.psi.ch")
    return RFSoC, LTDLC, magneticIR, ITCD