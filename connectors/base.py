"""
Base connector for any other processor connectors
Has a `add` that is override by specific connector to add data into connector
"""
from utils import get_logger_config

logger = get_logger_config(__name__)

class BaseConnector:

    def add(self, data):
        logger.debug(f"connector-base: {data}")



