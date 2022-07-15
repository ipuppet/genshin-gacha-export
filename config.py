import json
from utils import logger


class Config:
    setting = {
        "archive": True,
        "export_html": True,
        "export_xlsx": True,
        "export_uigf_json": True,
        "url": "",
    }
    path = ""

    def __init__(self, path="config.json"):
        self.path = path
        try:
            self.read()
        except:
            logger.warning("config not found")
        self.save()

    def read(self):
        f = open(self.path, "r", encoding="utf-8")
        self.setting.update(json.loads(f.read()))
        f.close()

    def setKey(self, key, value=None):
        self.setting[key] = value
        self.save()

    def getKey(self, key):
        try:
            return self.setting[key]
        except KeyError:
            return None

    def delKey(self, key):
        try:
            del self.setting[key]
        except KeyError:
            pass
        self.save()

    def save(self):
        f = open(self.path, "w", encoding="utf-8")
        f.write(
            json.dumps(self.setting, sort_keys=True, indent=4, separators=(",", ":"))
        )
        f.close()
