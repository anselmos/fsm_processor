from utils import get_logger_config
from connectors.base import BaseConnector
from connectors.db.models import Base, File

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logger = get_logger_config(__name__)

class PGConnector(BaseConnector):
    def __init__(self):
        self.engine = self.get_engine()

    def get_engine(self):
        # TODO update to config file of db!
        return create_engine("sqlite:///db.sqlite", echo=True)

    def create_db(self):
        """
        Should only be invokes at initialization
        """
        Base.metadata.create_all(self.engine)

    def add(self, data):
        super().add(data)
        logger.debug(f"pg-add : {data}")
        with Session(self.engine) as session:
            session.add(File(**data))
            session.commit()
