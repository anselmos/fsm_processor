from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from connectors.base import BaseConnector
from connectors.db.models import Base, File, Image
from constants import DB_URL, DB_ECHO
from utils import get_logger_config

logger = get_logger_config(__name__)

class PGConnector(BaseConnector):
    def __init__(self):
        self.engine = self.get_engine()

    def get_engine(self):
        return create_engine(DB_URL, echo=DB_ECHO)

    def create_db(self):
        """
        Should only be invokes at initialization
        """
        File.metadata.create_all(self.engine)
        Image.metadata.create_all(self.engine)

    def get_session(self):
        return Session(self.engine)

    def add(self, data):
        super().add(data)
        logger.debug(f"pg-add : {data}")
        with self.get_session() as session:
            session.add(File(**data))
            session.commit()

    def add_in_batch(self, data_list):
        with self.get_session() as session:
            logger.debug(data_list)
            session.add_all([File(**element) for element in data_list])
            session.commit()

    def get_query(self, model):
        session = self.get_session()
        return session.query(model)
