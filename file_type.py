from processors import read_extension
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

# FIXME move this into BaseFileProcessor!!
class FileType:
    def __init__(self, file_path: str=None):
        self.file_path = file_path
        self.extension = read_extension(file_path)

    def get_processor(self):
        processor = FILE_TYPES_TO_PROCESSOR.get(self.extension, None)
        if not processor:
            logger.warn(f"No processor for this type of file yet. Tried: {self.extension}")
            processor = FILE_TYPES_TO_PROCESSOR.get("")
        return processor