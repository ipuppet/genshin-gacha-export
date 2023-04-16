import json
import time
import requests
from urllib import parse
import os
import re
import shutil
from config import config, gachaTypeDict
from time import sleep
import traceback
from utils import logger
from path import DataPath


class Genshan:
    def __init__(self, url, wishTypes) -> None:
        self.url = self.toApi(url)
        self.wishTypes = wishTypes

    def toApi(self, url):

        logger.debug(url)

        spliturl = str(url).split("?")
        if "webstatic-sea" in spliturl[0] or "hk4e-api-os" in spliturl[0]:
            spliturl[
                0
            ] = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog"
        else:
            spliturl[0] = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog"
        url = "?".join(spliturl)
        return url

    def checkApi(self):
        if "?" not in self.url:
            logger.error("invalid url")
            return False

        try:
            r = requests.get(self.url)
            s = r.content.decode("utf-8")
            j = json.loads(s)
        except Exception:
            logger.error(traceback.format_exc())
            return False

        logger.debug(j)

        if not j["data"]:
            logger.warning(j["message"])
            return False
        return True

    def getApi(self, gachaType, size, page, end_id=""):
        parsed = parse.urlparse(self.url)
        querys = parse.parse_qsl(str(parsed.query))
        param_dict = dict(querys)
        param_dict["size"] = size
        param_dict["gacha_type"] = gachaType
        param_dict["page"] = page
        param_dict["lang"] = "zh-cn"
        param_dict["end_id"] = end_id
        param = parse.urlencode(param_dict)
        path = str(self.url).split("?")[0]
        api = path + "?" + param
        return api

    def getGachaLogs(self, gachaTypeId):
        # api 限制一页最大 20
        size = "20"
        gachaList = []
        end_id = "0"
        for page in range(1, 9999):

            logger.info(f"getting: {gachaTypeDict[gachaTypeId]}, page: {page}")

            api = self.getApi(gachaTypeId, size, page, end_id)
            r = requests.get(api)
            s = r.content.decode("utf-8")
            j = json.loads(s)
            gacha = j["data"]["list"]
            if not len(gacha):
                break
            for i in gacha:
                gachaList.append(i)
            end_id = j["data"]["list"][-1]["id"]
            sleep(0.5)

        return gachaList

    def mergeData(self, localData, gachaData):
        for type in gachaTypeDict:
            localGachaLog = []
            thisGachaLog = []
            try:
                localGachaLog = localData["gachaLog"][type]
                thisGachaLog = gachaData["gachaLog"][type]
            except:
                pass
            if thisGachaLog == localGachaLog:
                pass
            else:
                flag = [1] * len(thisGachaLog)
                loc = [[i["time"], i["name"]] for i in localGachaLog]
                for i in range(len(thisGachaLog)):
                    gachaGet = thisGachaLog[i]
                    get = [gachaGet["time"], gachaGet["name"]]
                    if get in loc:
                        pass
                    else:
                        flag[i] = 0

                tempData = []
                for i in range(len(thisGachaLog)):
                    if flag[i] == 0:
                        gachaGet = thisGachaLog[i]
                        tempData.insert(0, gachaGet)
                logger.info(
                    "merge {} added: {}".format(gachaTypeDict[type], len(tempData))
                )
                for i in tempData:
                    localData["gachaLog"][type].insert(0, i)

        return localData

    def load(self):
        if not self.checkApi():
            return

        self.startTime = time.strftime("%Y%m%d%H%M%S", time.localtime())

        gachaData = {}
        gachaData["gachaLog"] = {}
        for gachaTypeId in self.wishTypes:
            gachaLog = self.getGachaLogs(gachaTypeId)
            gachaData["gachaLog"][gachaTypeId] = gachaLog

        uid_flag = 1
        for gachaType in gachaData["gachaLog"]:
            for log in gachaData["gachaLog"][gachaType]:
                if uid_flag and log["uid"]:
                    gachaData["uid"] = log["uid"]
                    uid_flag = 0

        self.uid = gachaData["uid"]
        localDataFilePath = os.path.join(DataPath, f"gachaData-{self.uid}.json")

        if os.path.isfile(localDataFilePath):
            with open(localDataFilePath, "r", encoding="utf-8") as f:
                localData = json.load(f)
            self.data = self.mergeData(localData, gachaData)
        else:
            self.data = gachaData

        self.data["gachaType"] = gachaTypeDict

    def save(self):
        # 抽卡报告读取 gachaData.json
        # with open(os.path.join(DataPath, "gachaData.json"), "w", encoding="utf-8") as f:
        #     json.dump(mergeData, f, ensure_ascii=False, sort_keys=False, indent=4)
        # 待合并数据 gachaData-{uid}.json
        with open(
            os.path.join(DataPath, f"gachaData-{self.uid}.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(self.data, f, ensure_ascii=False, sort_keys=False, indent=4)
        # 备份历史数据 gachaData-{uid}-{self.startTime}.json
        with open(
            os.path.join(DataPath, f"gachaData-{self.uid}-{self.startTime}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(self.data, f, ensure_ascii=False, sort_keys=False, indent=4)

        if config.getKey("auto_archive"):
            logger.info("archive files")
            archive_path = os.path.join(DataPath, "archive")
            if not os.path.exists(archive_path):
                os.mkdir(archive_path)

            logger.debug("archive path: {}".format(archive_path))

            files = os.listdir(DataPath)
            archive_UIGF = [
                f for f in files if re.match(r"UIGF_gachaData-\d+-\d+.json", f)
            ]
            archive_json = [f for f in files if re.match(r"gachaData-\d+-\d+.json", f)]
            archive_xlsx = [
                f for f in files if re.match(r"gachaExport-\d+-\d+.xlsx", f)
            ]
            archive_files = archive_UIGF + archive_json + archive_xlsx

            logger.debug("files: {}".format(archive_files))

            for file in archive_files:
                try:
                    shutil.move(os.path.join(DataPath, file), archive_path)
                    logger.info("done: {}".format(file))
                except Exception:
                    logger.error("failed: {}".format(file))
                    logger.debug(traceback.format_exc())
                    try:
                        os.remove(os.path.join(archive_path, file))
                    except:
                        pass

    def export(self):
        if config.getKey("export_uigf_json"):
            import export_uigf

            export_uigf.write(self.uid, self.data, self.startTime)

        if config.getKey("export_xlsx"):
            import export_xlsx

            export_xlsx.write(self.uid, self.data, self.startTime)

        if config.getKey("export_html"):
            import export_html

            export_html.write(self.uid, self.data)

    def main(self):
        logger.info("start")
        self.load()
        self.save()
        self.export()


if __name__ == "__main__":
    gs = Genshan(config.getKey("url"), config.getKey("wish_types"))

    gs.main()
