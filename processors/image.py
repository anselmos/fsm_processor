from processors.base import BaseFileProcessor
from utils import get_logger_config
from PIL import Image, ExifTags, UnidentifiedImageError
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


    def get_data(self):
        super().get_data()

    def read_image_data(self):
        try:
            image_data = Image.open(self.file_path)
            exif = self.read_image_exif_data(image_data)
            if 'DateTime' in exif.keys():
                found_date = exif.get('DateTime')
            elif 'DateTimeOriginal' in exif.keys():
                found_date = exif.get('DateTimeOriginal')
        except (UnidentifiedImageError, OSError):
            pass

    def read_image_exif_data(self, image: Image):
        exif = {}
        try:
            exif_items = image._getexif()
        except AttributeError:
            exif_items = None
        if exif_items is not None:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in exif_items.items()
                if k in ExifTags.TAGS
            }
        return exif