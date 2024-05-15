import hashlib
from os import path as os_path, stat as os_stat

from connectors.db.models import File
from connectors.pg import PGConnector
from constants import PATH_CLEAN
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
        self.connector = PGConnector()
        if file_path and not self.has_path():
            ## FIXME update with proper connector based on config!
            self.md5sum = self.md5checksum(self.file_path)
            self.data = self.get_data()

    def process(self):
        logger.info(f"processing: {self.file_path}")
        if not self.has_path():
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

    def get_size(self):
        return int(os_stat(self.file_path).st_size)

    def get_created(self):
        return int(os_stat(self.file_path).st_ctime)

    def get_modified(self):
        return int(os_stat(self.file_path).st_mtime)

    def is_duplicated(self):
        query = self.connector.get_query(File)
        return isinstance(query.filter(File.md5sum == self.md5sum).first(), File)

    def has_path(self):
        query = self.connector.get_query(File)
        return isinstance(query.filter(File.path == self.file_path).first(), File)

    def get_data(self):
        return {
            'name': self.get_name(),
            'extension': read_extension(self.file_path),
            'path': self.file_path,
            'md5sum': self.md5sum,
            'clean': PATH_CLEAN,
            'duplicated_md5': self.is_duplicated(),
            'size': self.get_size(),
            'created': self.get_created(),
            'modified': self.get_modified(),

        }
