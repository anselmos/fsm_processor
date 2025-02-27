import hashlib
from os import path as os_path, stat as os_stat

from connectors.base import BaseConnector
from connectors.db.models import File
from connectors.pg import PGConnector
from constants import PATH_CLEAN
from processors import read_extension
from utils import get_logger_config
from datetime import datetime

logger = get_logger_config(__name__)


class BaseFileProcessor:

    EXTENSIONS_ALLOWED = []

    def file_type_items(self):
        items = {}
        for extension in self.EXTENSIONS_ALLOWED:
            items[extension] = self.__class__
        return items

    def __init__(self, file_path: str=None):
        self.file_path = file_path

        # TODO !! checking if path is in DB
        # if file_path and not self.has_path():
        #     ## FIXME update with proper connector based on config!
        #     if not os_path.exists(self.file_path):
        #         return
        #     self.md5sum = self.md5checksum(self.file_path)
        #     self.data = self.get_data()

    def process_md5(self):
        if not self.file_path or not os_path.exists(self.file_path):
            return
        try:
            self.md5sum = self.md5checksum(self.file_path)
        except Exception as e:
            logger.error(f"ERROR: could not read md5sum for file: {self.file_path}, with error: {e}")

    def process(self):
        logger.info(f"processing: {self.file_path}")
        if os_path.exists(self.file_path):
            return self.get_data()
        # TODO !! checking if path is in DB
        # if not self.has_path() and os_path.exists(self.file_path):
        #     self.connector.add(self.data)

    def get_name(self):
        return os_path.split(self.file_path)[-1]

    def md5checksum(self, filename):
        # based on https://stackoverflow.com/a/3431838
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_size(self):
        return int(os_stat(self.file_path).st_size)

    def get_created(self):
        return int(os_stat(self.file_path).st_ctime)

    def get_modified(self):
        return int(os_stat(self.file_path).st_mtime)

    def is_duplicated(self):
        query = self.connector.get_query(File)
        return isinstance(query.filter(File.md5sum == self.md5sum).first(), File)

    def has_path(self, db_connector: BaseConnector):
        session = db_connector.get_session()
        query = session.query(File)
        has_path_data = isinstance(query.filter(File.path == self.file_path).first(), File)
        session.close()
        return has_path_data

    def find_date_by_file_name(self, file_name):
        # TODO move to Image/Video processor!
        vid_name = file_name.split('VID_')
        # FIXME ValueError: time data 'zoom_0' does not match format '%d.%m.%Y,'
        if vid_name and len(vid_name) == 2:
            date_by_vid_name = vid_name[1].split(".")[0]
            return datetime.strptime(date_by_vid_name[:-3], '%Y%m%d_%H%M%S')

        mp4_name = file_name.split(".mp4")
        if len(mp4_name) > 1:
            mp4_name = mp4_name[0]
            mp4_date = None

            try:
                year_month_day_hour_minute_second_theme = '%Y%m%d_%H%M%S'
                mp4_date = datetime.strptime(mp4_name, year_month_day_hour_minute_second_theme)
            except ValueError:
                pass
            if mp4_date:
                return mp4_date
            space_mp4 = mp4_name.split(" ")
            try:
                mp4_date = datetime.strptime(space_mp4[1], '%d.%m.%Y,')
            except:
                try:
                    mp4_date = datetime.strptime(mp4_name, '%d.%m.%Y,')
                except:
                    logger.debug(f'ERROR mp4 no date detected {mp4_name}')
                    return None
            return mp4_date

    def get_data(self):
        logger.debug("started: get_data")
        extension = read_extension(self.file_path)
        exif_data = self.get_exiftool_data()
        date_created = self.get_date_created()
        if date_created:
            date_created = date_created.timestamp()
        return {
            'name': self.get_name(),
            'extension': extension,
            'path': self.file_path,
            'md5sum': self.md5sum,
            'clean': PATH_CLEAN,
            'size': self.get_size(),
            'created': self.get_created(),
            'modified': self.get_modified(),
            'date_created': date_created,
            'exiftool_data': exif_data,
            'File_FileModifyDate': exif_data.get('File:FileModifyDate', ''),
            'EXIF_ModifyDate': exif_data.get('EXIF:ModifyDate', ''),
            'EXIF_DateTimeOriginal': exif_data.get('EXIF:DateTimeOriginal', ''),
        }

    def get_date_created(self) -> datetime:
        """
        Date created as datetime.
        Defaults to 1970.
        """
        return datetime.fromtimestamp(0)

    def get_exiftool_data(self) -> dict:
        return {}

