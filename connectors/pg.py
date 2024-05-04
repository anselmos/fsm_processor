from utils import get_logger_config
from connectors.base import BaseConnector

logger = get_logger_config(__name__)

class PGConnector(BaseConnector):

    def add(self, data):
        super().add()
        logger.debug(f"pg-add : {data}")
