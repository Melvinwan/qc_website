from Toptica_ophyd import LaserToptica
from XMLGenerator import xml_config_to_dict
toptica_host = xml_config_to_dict("staticfiles/toptica.xml")
LTDLC = LaserToptica(prefix="...",name="LTDLC",config_host=toptica_host)

import time
while True:
    print(LTDLC.try_connect())
    time.sleep(1)