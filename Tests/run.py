from WLED import Wled
import time
import json

settings = json.load(open("Config.json"))



strip = Wled(settings["Wled_IP"], settings["Api_Endpoint"] or "/json")
strip.set_seg(0)
strip.set_color([255, 0, 0])
time.sleep(2)
strip.set_color([255, 255, 255])
print(strip.get_raw_data())