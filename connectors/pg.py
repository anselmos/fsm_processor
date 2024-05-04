from utils import get_logger_config
from connectors.base import BaseConnector
from connectors.db.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logger = get_logger_config(__name__)

class PGConnector(BaseConnector):

    def get_engine(self):
        return create_engine("sqlite:///db.sqlite", echo=True)

    def create_db():
        """
        Should only be invokes at initialization
        """
        Base.metadata.create_all(self.get_engine())

    def add(self, data):
        super().add()
        logger.debug(f"pg-add : {data}")
        engine = self.get_engine()
        with Session(engine) as session:
            session.add(File(**data))
            session.commit()
