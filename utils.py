import sys

import platform
import traceback
from loguru import logger
from path import BasePath, LogFilePath


open(LogFilePath, "w").close()
config = {
    "handlers": [
        {"sink": sys.stdout, "level": "INFO"},
        {"sink": LogFilePath, "level": "DEBUG"},
    ],
}
logger.configure(**config)

logger.debug("BasePath: {}", BasePath)


def pressAnyKeyToExit(msg="Press any key to exit."):
    from sys import exit

    logger.info(msg)
    try:
        if platform.system() == "Windows":
            from msvcrt import getch

            getch()
        else:
            input()
    except KeyboardInterrupt:
        exit()
    except Exception:
        logger.error(traceback.format_exc())
    exit()
