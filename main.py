from kafka import KafkaConsumer, TopicPartition
import argparse

from constants import KAFKA_TOPIC
from file_type import FileType
from processors.base import BaseFileProcessor
from utils import get_logger_config
import json

logger = get_logger_config(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Partition", help = "Partition id")
    args = parser.parse_args()

    partition_id = 0
    if args.Partition:
        partition_id = int(args.Partition)

    logger.debug("Process of processing started. Waiting for upcoming kafka file-path values.")
    # TODO - change from hardcoded group-id.
    consumer = KafkaConsumer(
        group_id='my-group',
        bootstrap_servers=['localhost:9092'],
        api_version=(3, ),
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    consumer.assign([TopicPartition(KAFKA_TOPIC, partition_id)])
    for message in consumer:
        data = message.value
        file_path = data['path']
        logger.debug(file_path)
        processor = FileType(file_path).get_processor()
        # TODO add response from processor-process to save this with ELK.
        processor(file_path).process()
        # TODO elk save with protobuf grpc.

