import hashlib
from os import path as os_path

from connectors.pg import PGConnector
from processors import read_extension
from utils import get_logger_config

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
        if file_path:
            self.data = self.get_data()
            ## FIXME update with proper connector based on config!
            self.connector = PGConnector()

    def process(self):
        logger.info(f"processing: {self.file_path}")
        self.connector.add(self.data)

    def get_name(self):
        return os_path.split(self.file_path)[-1]

    def md5checksum(self, filename):
        # based on https://stackoverflow.com/a/3431838
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_data(self):
        return {
            'name': self.get_name(),
            'extension': read_extension(self.file_path),
            'path': self.file_path,
            'md5sum': self.md5checksum(self.file_path),
            'clean': True,
        }
