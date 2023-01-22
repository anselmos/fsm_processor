from kafka import KafkaConsumer
from constants import KAFKA_TOPIC

if __name__ == '__main__':
    consumer = KafkaConsumer(KAFKA_TOPIC, group_id='my-group', bootstrap_servers=['localhost:9092'], api_version=(3, ))
    for message in consumer:
        print(message.value)
