import sys
import os
import time
import requests
todo_func = [
#    "__init__",
#    "on",
#    "off",
#    "update",
#    "get_info",
#    "toggle",
#    "set_brightness",
#    "set_color",
    "set_effect",
    "set_color_palette",
    "create_segment",
    "delete_segment",
    "create_preset",
    "delete_preset",
    "use_preset",
#    "set_secondary_color",
#    "set_thirdary_color",
    "get_effects",
    "get_color_palettes",
    "get_effect",
    "get_color_palette"
]
class Wled():
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.raw_data = requests.get(f"http://{hostname}/json/").json()["state"]
    def update(self):
        self.raw_data = requests.get(f"http://{self.hostname}/json/").json()["state"]
        self.data = self.raw_data["seg"][self.seg]
    def get_raw_data(self):
        self.raw_data = requests.get(f"http://{self.hostname}/json/").json()["state"]
        self.data = self.raw_data["seg"][self.seg]
        return(self.raw_data)
    def on(self):
        self.data["on"] = True
        requests.post(f"http://{self.hostname}/json/", json={"on": True})
    def off(self):
        self.data["on"] = False
        requests.post(f"http://{self.hostname}/json/", json={"on": False})
    def toggle(self):
        requests.post(f"http://{self.hostname}/json/", json={"seg": ([{}]*self.seg)+[{"on": not(self.data["on"])}]})
    def set_brightness(self, brightness: int):
        self.data["bri"] = brightness
        requests.post(f"http://{self.hostname}/json/", json={"seg": ([{}]*self.seg)+[{"bri": brightness}]})
    def set_color(self, color: list):
        col = [color, self.data["col"][1], self.data["col"][2]]
        requests.post(f"http://{self.hostname}/json/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_secondary_color(self, color: tuple):
        col =[self.data["col"][0], color, self.data["col"][2]]
        requests.post(f"http://{self.hostname}/json/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_thirdadary_color(self, color: tuple):
        col = [self.data["col"][0], self.data["col"][1], color]
        requests.post(f"http://{self.hostname}/json/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_seg(self, seg: int):
        if hasattr(self, "seg") and hasattr(self, "data"):
            self.raw_data["seg"][self.seg] = self.data
        self.data = self.raw_data["seg"][seg]
        self.seg = seg
d = Wled("carson-desk.local")
d.set_seg(0)
d.set_color([255, 0, 0])
print(d.get_raw_data())
time.sleep(2)
d.set_color([255, 255, 255])
print(d.get_raw_data())