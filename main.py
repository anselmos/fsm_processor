import argparse
import json

from kafka import KafkaConsumer, TopicPartition

from connectors.pg import PGConnector
from constants import INIT_PATH, KAFKA_HOST, KAFKA_PORT, KAFKA_GROUP_ID
from constants import KAFKA_TOPIC
from file_type import FileType
from utils import get_logger_config, enumerate_files
from utils import get_paths_redis

logger = get_logger_config(__name__)

def process_file(file_path, using_redis=False, redis_connector=None):
    if using_redis and redis_connector and redis_connector.get(file_path) is not None:
        logger.debug(f'Skipping file {file_path}')
        return False
    logger.debug(file_path)
    processor_classname = FileType(file_path).get_processor()
    processor = processor_classname(file_path)
    # TODO add response from processor-process to save this with ELK.
    processor.process_md5()
    return processor.process()

def with_kafka(partition_id):
    logger.debug("Process of processing started. Waiting for upcoming kafka file-path values.")
    # TODO - change from hardcoded group-id.
    consumer = KafkaConsumer(
        group_id=KAFKA_GROUP_ID,
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        api_version=(3, ),
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    consumer.assign([TopicPartition(KAFKA_TOPIC, partition_id)])

    pg_connector = PGConnector()

    for message in consumer:
        data = message.value
        if 'batch' in data.keys():
            batch_paths = data['batch']
            file_data_per_batch = []
            for file_path in batch_paths:
                try:
                    file_data = process_file(file_path, using_redis=False)
                    if file_data:
                        file_data_per_batch.append(file_data)
                except Exception as e:
                    logger.debug(f"ERROR processing file (parsing): {file_path}, error: {e}")
            pg_connector.add_in_batch(file_data_per_batch)

                # TODO elk save with protobuf grpc.
        elif 'file' in data.keys():
            file_path = data['file']
            file_data = process_file(file_path)
            pg_connector.add_in_batch([file_data])

def without_kafka():
    logger.debug("Process of processing started. Iterating file-path values.")
    pg_connector = PGConnector()
    file_data_per_batch = []
    redis_connector = get_paths_redis()
    for file_path in enumerate_files(INIT_PATH):
        # try:
        file_data = process_file(file_path, True, redis_connector)
        if file_data is not False:
            logger.debug(f"processed file. adding to database {file_path}")
            pg_connector.add(file_data)
            redis_connector.set(file_path, file_path)
        else:
            logger.debug("enumerate files if-ELSE in else")
        # except Exception as e:
        #     logger.debug(f"ERROR processing file (parsing): {file_path}, error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Partition", help = "Partition id")
    parser.add_argument("-kafka", "--Kafka", help = "To run with Kafka. Value needs to be either 1 or True or no value but adding -kafka")
    args = parser.parse_args()

    partition_id = 0
    run_with_kafka = False
    if args.Partition:
        partition_id = int(args.Partition)
    run_with_kafka = True if args.Kafka and (args.Kafka == "1" or args.Kafka == 'True') else False
    if run_with_kafka:
        with_kafka(partition_id)
    else:
        without_kafka()

    print(run_with_kafka, partition_id)