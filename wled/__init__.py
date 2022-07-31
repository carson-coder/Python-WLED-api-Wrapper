import requests as rq
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# code = on on off on update

requests = rq.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
requests.mount('http://', adapter)
requests.mount('https://', adapter)
if __name__ == "__main__":
    import Exceptions
else:
    from . import Exceptions
import json

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
#    "create_segment",
#    "delete_segment",
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
    info = json.load(open('./wled/config.json'))
    version = f"{info['version']}: {(int(info['stable']) * 'stable') + (int(not(info['stable'])) * 'beta')}"
    def __init__(self, hostname: str, endpoint: str = "/json/", error=True):
        self.codes = []
        self.hostname = hostname.replace("http://", "").replace("https://", "")
        self.endpoint = endpoint.replace("/", "")
        self.error = error
        try:
            self.raw_raw_data = requests.get(f"http://{self.hostname}/{self.endpoint}/").json()
        except Exception as e:
            if error:
                raise Exceptions.InvalidHost(f"http://{self.hostname}/{self.endpoint}/ is not a valid host")
            return Exceptions.InvalidHost(f"http://{self.hostname}/{self.endpoint}/ is not a valid host")
        self.raw_data = self.raw_raw_data["state"]
    def update(self):
        self.code(self.update)
        self.raw_raw_data = requests.get(f"http://{self.hostname}/{self.endpoint}/").json()
        self.raw_data = self.raw_raw_data["state"]
        if hasattr(self, "seg") and hasattr(self, "data"):
            self.data = self.raw_data["seg"][self.seg]
    def get_raw_data(self):
        self.codes = []
        self.raw_raw_data = requests.get(f"http://{self.hostname}/{self.endpoint}/").json()
        self.raw_data = self.raw_raw_data["state"]
        if hasattr(self, "seg") and hasattr(self, "data"):
            self.data = self.raw_data["seg"][self.seg]
        return(self.raw_raw_data)
    def on(self):
        self.codes.append("on")
        self.data["on"] = True
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"on": True})
    def off(self):
        self.codes.append("off")
        self.data["on"] = False
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"on": False})
    def toggle(self):
        self.codes = []
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"on": not(self.data["on"])}]})
    def set_brightness(self, brightness: int):
        self.codes = []
        self.data["bri"] = brightness
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"bri": brightness}]})
    def set_color(self, color: list):
        self.codes = []
        col = [color, self.data["col"][1], self.data["col"][2]]
        self.data["col"] = col
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_secondary_color(self, color: tuple):
        self.codes = []
        col =[self.data["col"][0], color, self.data["col"][2]]
        self.data["col"] = col
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_thirdadary_color(self, color: tuple):
        self.codes = []
        col = [self.data["col"][0], self.data["col"][1], color]
        self.data["col"] = col
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*self.seg)+[{"col": col}]})
    def set_seg(self, seg: int):
        self.codes = []
        if hasattr(self, "seg") and hasattr(self, "data"):
            self.raw_data["seg"][self.seg] = self.data
            
        if seg in range(0, len(self.raw_data["seg"])):
            self.seg = seg
            self.data = self.raw_data["seg"][self.seg]
            return
            
        if self.error:
            raise Exceptions.InvalidSegment(f"{seg} is not a valid segment")
        else:
            return Exceptions.InvaledSegment(f"{seg} is not a valid segment")
    def get_color_palettes(self):
        self.codes = []
        return(self.raw_raw_data["color_palettes"])
    def get_effects(self):
        self.codes = []
        return(self.raw_raw_data["effects"])
    def get_effect(self):
        self.codes = []
        return(self.raw_raw_data["effects"][self.data[effects]])
    def get_color_palette(self):
        self.codes = []
        return(self.raw_raw_data["palettes"][self.data[paletts]])
    def set_effect(self, fx: str):
        self.codes = []
        try:
            self.data["fx"] = self.raw_raw_data["effects"].index(fx)
            requests.post(f"http://{self.hostname}/{self.endpoint}/", json = {"seg": ([{}]*self.seg)+[{"fx": self.raw_raw_data["effects"].index(fx) }]})
        except ValueError:
            if self.error:
                raise Exceptions.InvalidFX(f"{fx} is not a valid effect")
            else:
                return Exceptions.InvalidFX(f"{self.data[effects]} is not a valid effect")
    def set_color_palette(self, pal: str):
        self.codes = []
        try:
            self.data["pal"] = self.raw_raw_data["effects"].index(pal)
            requests.post(f"http://{self.hostname}/{self.endpoint}/", json = {"seg": ([{}]*self.seg)+[{"pal": self.raw_raw_data["palettes"].index(pal) }]})
        except ValueError:
            if self.error:
                raise Exceptions.InvalidPalette(f"{self.data[paletts]} is not a valid palette")
            else:
                return Exceptions.InvalidPalette(f"{self.data[paletts]} is not a valid palette")
    def __str__(self):
        self.codes = []
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
        self.codes = []
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"ps": preset_id})
    def create_segment(self, brightness: int, color1: tuple, color2: tuple, color3: tuple, start: int | None, end: int | None, range: list | None):
        self.codes = []
        if (start != None) and (end != None) and range == None:
            pass
        elif start and end and range:
            if self.error:
                raise Exceptions.InvalidRange(f"Cant have start, end and range at the same time")
            else:
                print("Cant have start, end and range at the same time")
        elif range:
            start = range[0]
            end = range[1]
        else:
            if self.error:
                raise Exceptions.InvalidRange(f"Need start and end or range")
            else:
                print("Need start and end or range")
                return(Exceptions.InvalidRange(f"Need start and end or range"))
        if len(self.raw_data["seg"]) == 0:
            self.raw_data["seg"] = [{"id": -1}]
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*len(self.raw_data["seg"]))+[{"id": self.raw_data['seg'][max(len(self.raw_data["seg"])-1, 0)]['id']+1, "on": True, "start": start, "stop": end, "bri": brightness, "col": [color1, color2, color3]}]})
        self.update()
    def delete_segment(self, id: int):
        self.codes = []
        for i in self.raw_data["seg"]+["err"]:
            if i == 'err':
                if self.error:
                    raise Exceptions.InvalidSegment(f"{id} is not a valid segment")
                else:
                    print("{id} is not a valid segment")
                    return(Exceptions.InvalidSegment(f"{id} is not a valid segment"))
            if i["id"] == id:
                b = self.raw_data["seg"].index(i)
                break
                
        requests.post(f"http://{self.hostname}/{self.endpoint}/", json={"seg": ([{}]*b)+[{"on": True, "start": 1, "stop": 0}]})
        self.update()
    def code(self, code):
        if code != self.update:
            print("You need the code")
            self.codes = []
            return
        if self.codes == ["on","on","off","on"]:
            print("rainbowroad")
            self.set_effect("Rainbow")
            self.set_color_palette("Rainbow")
            self.set_color((255,0,0))
            self.set_secondary_color((0,255,0))
            self.set_thirdadary_color((0,0,255))
        self.codes = []