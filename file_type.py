from processors.image import ImageProcessor
from processors.unknown import UnknownFileProcessor
from processors.video import VideoProcessor
from utils import get_logger_config

FILE_TYPES_TO_PROCESSOR = {
    "": UnknownFileProcessor,
}
FILE_TYPES_TO_PROCESSOR.update(ImageProcessor().file_type_items())
FILE_TYPES_TO_PROCESSOR.update(VideoProcessor().file_type_items())
logger = get_logger_config(__name__)


class FileType:
    def __init__(self, file_path: str=None):
        self.file_path = file_path
        self.extension = self.read_extension()

    def read_extension(self):
        # TODO make it more advanced by checking file header in future.
        logger.debug("reading extension")
        splited_by_dot = self.file_path.split(".")
        if len(splited_by_dot) == 2:
            return splited_by_dot[-1].upper()
        else:
            logger.warn("MULTIPLE FILE EXTENSION DETECTED IN FILE NAME.")
            return splited_by_dot[-1].upper()

    def get_processor(self):
        processor = FILE_TYPES_TO_PROCESSOR.get(self.extension, None)
        if not processor:
            logger.warn(f"No processor for this type of file yet. Tried: {self.extension}")
            processor = FILE_TYPES_TO_PROCESSOR.get("")
        return processor