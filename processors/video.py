from processors.base import BaseFileProcessor
from utils import get_logger_config

logger = get_logger_config(__name__)

class VideoProcessor(BaseFileProcessor):
    EXTENSIONS_ALLOWED = [
        "AVI", "3GP", "MP4"
    ]
    def process(self):
        super().process()

