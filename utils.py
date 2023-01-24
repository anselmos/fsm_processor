import logging
import logging.config
from datetime import datetime

def get_logger_config(name=None):
    logging.config.fileConfig('logging.conf', defaults={
        "log_date": datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    })
    return logging.getLogger(name)