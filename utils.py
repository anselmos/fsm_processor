import logging
import logging.config


def get_logger_config(name=None):
    logging.config.fileConfig('logging.conf')
    return logging.getLogger(name)