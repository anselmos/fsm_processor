from processors.base import BaseFileProcessor
from utils import get_logger_config

logger = get_logger_config(__name__)


class ArchiveProcessor(BaseFileProcessor):
    EXTENSIONS_ALLOWED = [
        "GZ", "RAR", "ZIP"
    ]

    def process(self):
        logger.debug("ARCHIVE DETECTED!")
        return super().process()

    def get_date_created(self):
        return self.find_date_by_file_name(self.get_name())

