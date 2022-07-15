import os
import sys


def initPath(path):
    if not os.path.exists(path):
        os.mkdir(path)


BasePath = os.path.dirname(os.path.realpath(sys.argv[0]))

LogPath = os.path.join(BasePath, "log")
initPath(LogPath)
LogFilePath = os.path.join(LogPath, "genshin.log")

ConfigPath = os.path.join(BasePath, "config")
initPath(ConfigPath)
ConfigFilePath = os.path.join(ConfigPath, "config.json")

DataPath = os.path.join(BasePath, "data")
initPath(DataPath)
GachaReportFilePath = os.path.join(DataPath, "gachaReport.html")
