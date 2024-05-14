from utils import get_logger_config

logger = get_logger_config(__name__)


def read_extension(file_path):
    # TODO make it more advanced by checking file header in future.
    logger.debug("reading extension")
    splited_by_dot = file_path.split(".")
    if len(splited_by_dot) == 2:
        return splited_by_dot[-1].upper()
    else:
        logger.warn("MULTIPLE FILE EXTENSION DETECTED IN FILE NAME.")
        return splited_by_dot[-1].upper()