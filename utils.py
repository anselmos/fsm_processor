import logging
import logging.config
import pickle
from datetime import datetime

import exiftool
import redis

from constants import REDIS_HOST, REDIS_PASSWORD


def get_logger_config(name=None):
    logging.config.fileConfig('logging.conf', defaults={
        "log_date": datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    })
    return logging.getLogger(name)

def get_paths_redis():
    return redis.Redis(
        host=REDIS_HOST, port=30036, password=REDIS_PASSWORD,
        decode_responses=True, db=0)

def exiftool_metadata(file_path):
    logger = get_logger_config(__name__)
    logger.debug("started: get_exiftool_data")
    try:
        return exiftool.ExifToolHelper().get_metadata(file_path)[0]
    except Exception as e:
        logger.error(f"ERROR: could not read exiftool data for file: {file_path}, with error: {e}")
        logger.debug("ended: get_exiftool_data")
        return {}


# def save_pickle
def load_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def save_pickle(filename, object):
    with open(filename, "wb") as f:
        pickle.dump(object, f)