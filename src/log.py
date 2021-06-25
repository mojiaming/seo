import logging
import os
logger = logging.getLogger()
fh = logging.FileHandler(os.getcwd() + "\\run.log", encoding="utf-8", mode="a")
formatter = logging.Formatter("%(asctime)s - %(name)s-%(levelname)s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)
from pubsub import pub


def info(msg):
    logger.info(msg)
    pub.sendMessage('update_log')


def error(msg):
    logger.error(str(msg))
    pub.sendMessage('update_log')


def close():
    fh.close()
