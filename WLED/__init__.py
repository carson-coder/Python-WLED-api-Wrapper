import requests
from . import Exceptions

paletts = "pal"
effects = "fx"
todo_func = [
#    "__init__",
#    "on",
#    "off",
#    "update",
#    "get_info",
#    "toggle",
#    "set_brightness",
#    "set_color",
#    "set_effect",
#    "set_color_palette",
    "create_segment",
    "delete_segment",
    "create_preset",
    "delete_preset",
    "use_preset",
#    "set_secondary_color",
#    "set_thirdary_color",
#    "get_effects",
#    "get_color_palettes",
#    "get_effect",
#    "get_color_palette"
]
class Wled():
    def __init__(self, hostname: str, endpoint: str = "/json/"):
        self.hostname = hostname.replace("http://", "").replace("https://", "")
        self.endpoint = endpoint.replace("/", "")
        self.raw_raw_data = requests.get(f"http://{self.hostname}/{self.endpoint}/").json()
        self.raw_data = self.raw_raw_data["state"]
    def update(self):
        self.raw_raw_data = requests.get(f"http://{self.hostname}/{self.endpoint}/").json()
        self.raw_data = self.raw_raw_data["state"]
        self.data = self.raw_data["seg"][self.seg]
    def get_raw_data(self):
        self.raw_raw_data = requests.get(f"http://{self.hostname}/{self.endpoint}/").json()
        self.raw_data = self.raw_raw_data["state"]
        self.data = self.raw_data["seg"][self.seg]
        return(self.raw_raw_data)
    def on(self):
        self.data["on"] = True
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"on": True})
    def off(self):
        self.data["on"] = False
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"on": False})
    def toggle(self):
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"on": not(self.data["on"])}]})
    def set_brightness(self, brightness: int):
        self.data["bri"] = brightness
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"bri": brightness}]})
    def set_color(self, color: list):
        col = [color, self.data["col"][1], self.data["col"][2]]
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_secondary_color(self, color: tuple):
        col =[self.data["col"][0], color, self.data["col"][2]]
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_thirdadary_color(self, color: tuple):
        col = [self.data["col"][0], self.data["col"][1], color]
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_seg(self, seg: int):
        if hasattr(self, "seg") and hasattr(self, "data"):
            self.raw_data["seg"][self.seg] = self.data
        self.data = self.raw_data["seg"][seg]
        self.seg = seg
    def get_color_palettes(self):
        return(self.raw_raw_data["color_palettes"])
    def get_effects(self):
        return(self.raw_raw_data["effects"])
    def get_effect(self):
        return(self.raw_raw_data["effects"][self.data[effects]])
    def get_color_palette(self):
        return(self.raw_raw_data["color_palettes"][self.data[paletts]])
    def set_effect(self):
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json = self.raw_raw_data["effects"].index(self.data[effects]))
    def set_color_palette(self):
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json = self.raw_raw_data["color_palettes"].index(self.data[paletts]))
    def __str__(self):
        return(f"""WLED Strip:
    IP: {self.hostname}
    Endpoint: {self.endpoint}
    Current Segment: {self.seg}:
        On: {self.data["on"]}
        Brightness: {self.data["bri"]}
        Color1: {self.data["col"][0]}
        Color2: {self.data["col"][1]}
        Color3: {self.data["col"][2]}
               """)
    def use_preset(self, preset_id: int):
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"state": {"ps": preset_id}})