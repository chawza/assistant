import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.logging import logger


db_url  = os.environ['ASSISTANT_POSTGRESQL_URL']
db_engine = create_engine(db_url, echo=True)

SessionLocal = sessionmaker(bind=db_engine)

logger.info(f'Database engine initialized using {db_url}')

def get_db_session():
    with SessionLocal() as session:
        yield session
