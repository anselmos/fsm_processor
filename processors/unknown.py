from processors.base import BaseFileProcessor
from utils import get_logger_config

logger = get_logger_config(__name__)


class UnknownFileProcessor(BaseFileProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        logger.warn(self.file_path)
        return super().process()
        # TODO save this extension in a log!
