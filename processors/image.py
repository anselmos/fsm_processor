from processors.base import BaseFileProcessor
from utils import get_logger_config, exiftool_metadata
from PIL import Image, ExifTags, UnidentifiedImageError
from datetime import datetime

logger = get_logger_config(__name__)


class ImageProcessor(BaseFileProcessor):
    EXTENSIONS_ALLOWED = [
        "PNG",
        "JPG",
        "JPEG",
        "IMG",
        "GIF",
        "BMP",
        "3GP",
    ]

    def process(self):
        logger.debug("IMAGE DETECTED!")
        return super().process()

    def get_date_created(self):
        found_date = None
        try:
            image_data = Image.open(self.file_path)
            exif = self.read_image_exif_data(image_data)
            if 'DateTime' in exif.keys():
                found_date = exif.get('DateTime')
            elif 'DateTimeOriginal' in exif.keys():
                found_date = exif.get('DateTimeOriginal')
        except (UnidentifiedImageError, OSError):
            pass
        if not found_date:
            pic_img_name = self.get_name().split("IMG_")
            if len(pic_img_name) > 1:
                pic_img_date = None
                try:
                    pic_img_date = datetime.strptime(pic_img_name[1][:-7], '%Y%m%d_%H%M%S')
                except ValueError:
                    try:
                        pic_img_date = datetime.strptime(self.get_name()[:15], '%Y%m%d_%H%M%S')
                    except ValueError:
                        pass
                return pic_img_date
            try:
                found_date = self.find_date_by_file_name(self.get_name())
            except ValueError as val_err:
                # print("VALUE ERROR", val_err)
                pass
        if isinstance(found_date, str):
            try:
                return datetime.strptime(found_date, "%Y:%m:%d %H:%M:%S")
            except:
                print("FOUND DATE NOT CONVERTED:(", found_date)
                return None
        return found_date

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

    def get_exiftool_data(self) -> dict:
        return exiftool_metadata(self.file_path)