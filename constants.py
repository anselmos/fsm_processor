import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'fsm_file_path')
DB_URL = os.getenv('DB_URL', 'sqlite:///db.sqlite')
DB_ECHO = bool(os.getenv('DB_ECHO', False))
PATH_CLEAN = bool(os.getenv('PATH_CLEAN', True))
