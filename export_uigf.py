import os
import time
import json
from gacha_metadata import gachaQueryTypeIds
from utils import logger
from path import DataPath


def id_generator():
    id = 1000000000000000000
    while True:
        id = id + 1
        yield str(id)


def convert(uid, gachaLog):

    logger.debug("convert UIGF")

    if "gachaLog" in gachaLog:
        logger.debug("gachaLog key already exists")
        gachaLog = gachaLog["gachaLog"]
    UIGF_data = {}
    UIGF_data["info"] = {}
    UIGF_data["info"]["uid"] = uid
    UIGF_data["info"]["lang"] = "zh-cn"
    UIGF_data["info"]["export_time"] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()
    )
    UIGF_data["info"]["export_app"] = "genshin-gacha-export"
    UIGF_data["info"]["export_app_version"] = ""
    UIGF_data["info"]["uigf_version"] = "v2.2"
    UIGF_data["info"]["export_timestamp"] = int(time.time())
    all_gachaDictList = []

    for gacha_type in gachaQueryTypeIds:
        gacha_log = gachaLog.get(gacha_type, [])
        gacha_log = sorted(gacha_log, key=lambda gacha: gacha["time"], reverse=True)
        gacha_log.reverse()
        for gacha in gacha_log:
            gacha["uigf_gacha_type"] = gacha_type
        all_gachaDictList.extend(gacha_log)
    all_gachaDictList = sorted(all_gachaDictList, key=lambda gacha: gacha["time"])

    id = id_generator()
    for gacha in all_gachaDictList:
        if gacha.get("id", "") == "":
            gacha["id"] = next(id)
    all_gachaDictList = sorted(all_gachaDictList, key=lambda gacha: gacha["id"])
    UIGF_data["list"] = all_gachaDictList

    logger.debug("done, count: {}", len(all_gachaDictList))

    return UIGF_data


def write(uid, gachaLog, t):
    logger.info("UIGF JSON")
    with open(
        os.path.join(DataPath, f"UIGF_gachaData-{uid}-{t}.json"),
        "w",
        encoding="utf-8",
    ) as f:
        UIGF_data = convert(uid, gachaLog)
        json.dump(UIGF_data, f, ensure_ascii=False, sort_keys=False, indent=4)
