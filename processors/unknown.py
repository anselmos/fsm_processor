import os
from processors.base import BaseFileProcessor
from utils import get_logger_config

RUN_ELK = os.getenv('RUN_ELK', False)

logger = get_logger_config(__name__)
from elasticsearch import helpers, Elasticsearch
from elasticsearch_dsl import Search

class UnknownFileProcessor(BaseFileProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cleanup_index(self):
        FORBIDDEN_CHARS = [' ', '"', '*', '\\', '<', '|', ',', '>', '/', '?']
        clean_index = self.file_path

        for forbidden_char in FORBIDDEN_CHARS:
            clean_index = clean_index.replace(forbidden_char, "").lower()
        return clean_index

    def process(self):
        super().process()
        # TODO save this extension in a log!
        logger.warn(self.file_path)
        if not RUN_ELK:
            return
        client = Elasticsearch('192.168.127.150', timeout=30)
        clean_index = self.cleanup_index()
        doc = {

            "_index": clean_index,
            "_type": "unknown_file",
            "_id": self.file_path,
            "_source": {
                "author": "FSM_PROCESSOR_UNKNOWN_FILE_PROCESSOR",
                "content": self.file_path,
            }
        }
        helpers.bulk(client, [doc])
