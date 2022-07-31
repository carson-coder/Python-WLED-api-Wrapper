from wled import Wled
import time
import json

settings = json.load(open("Tests/Config.json"))



strip = Wled(settings["Wled_IP"], settings["Api_Endpoint"] or "/json")
print(strip.get_raw_data())
strip.delete_segment(0)
print("del")
time.sleep(1)
strip.create_segment(brightness=255, color1=[255, 255, 255], color2=[0, 0, 0], color3=[0, 0, 0], start=0, end=20, range=None)
strip.set_seg(0)
strip.set_color([255, 0, 0])
strip.set_effect("Solid")
strip.create_segment(brightness=255, color1=[255, 255, 255], color2=[0, 0, 0], color3=[0, 0, 0], start=20, end=51, range=None)
strip.set_seg(1)
strip.set_color([0, 255, 255])
strip.set_effect("Solid")