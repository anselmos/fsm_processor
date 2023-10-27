from kafka import KafkaConsumer

from constants import KAFKA_TOPIC
from file_type import FileType
from utils import get_logger_config

logger = get_logger_config(__name__)

if __name__ == '__main__':
    logger.debug("Process of processing started. Waiting for upcoming kafka file-path values.")
    # TODO - change from hardcoded group-id.
    consumer = KafkaConsumer(KAFKA_TOPIC, group_id='my-group', bootstrap_servers=['localhost:9092'], api_version=(3, ))
    for message in consumer:
        file_path = message.value.decode("utf-8")
        logger.debug(file_path)
        processor = FileType(file_path).get_processor()
        # TODO add response from processor-process to save this with ELK.
        processor(file_path).process()
        # TODO elk save with protobuf grpc.

