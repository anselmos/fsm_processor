from processors.base import BaseFileProcessor
from utils import get_logger_config

logger = get_logger_config(__name__)


class ImageProcessor(BaseFileProcessor):
    EXTENSIONS_ALLOWED = [
        "PNG",
        "JPG",
        "JPEG",
        "IMG",
        "GIF",
        "BMP",
    ]

    def process(self):
        super().process()
        logger.debug("IMAGE DETECTED!")

