from processors.base import BaseFileProcessor
from utils import get_logger_config, exiftool_metadata

logger = get_logger_config(__name__)


class VideoProcessor(BaseFileProcessor):
    EXTENSIONS_ALLOWED = [
        "AVI", "3GP", "MP4", "MOV"
    ]

    def process(self):
        logger.debug("VIDEO DETECTED!")
        return super().process()

    def get_date_created(self):
        date_created = None
        try:
            date_created = self.find_date_by_file_name(self.get_name())
        except:
            pass

        return date_created

    def get_exiftool_data(self) -> dict:
        return exiftool_metadata(self.file_path)