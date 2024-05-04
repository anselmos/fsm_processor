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
        self.data = self.get_data()


    def process(self):
        logger.info(f"processing: {self.file_path}")

    def get_data(self):
        # TODO add based on File model!
        return {
            'path': self.file_path
        }
