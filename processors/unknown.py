from processors.base import BaseFileProcessor
from utils import get_logger_config
from connectors.base import BaseConnector

logger = get_logger_config(__name__)


class UnknownFileProcessor(BaseFileProcessor):
    def __init__(self, *args, **kwargs):
        self.connector = BaseConnector()
        super().__init__(*args, **kwargs)

    def process(self):
        super().process()
        # TODO save this extension in a log!
        logger.warn(self.file_path)
        ## FIXME update with proper connector based on config!
        self.connector.add(self.data)
