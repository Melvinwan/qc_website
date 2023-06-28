from ssh import SSH
from XMLGenerator import xml_config_to_dict
rfsoc_host = xml_config_to_dict("staticfiles/xilinx_host.xml")
print(rfsoc_host)
RFSoC = SSH(rfsoc_host["host"],rfsoc_host["username"],rfsoc_host["password"])
RFSoC.connect()
RFSoC.disconnect()