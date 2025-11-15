import os

from sqlmodel import create_engine, SQLModel
from src.db.models.users import User
import os

database_filepath = os.environ.get('DATABASE_PATH', 'db.sqlite3')
db_url = f'sqlite:///{database_filepath}'

db_engine = create_engine(db_url, connect_args={'check_same_thread': False})

# Create all tables
SQLModel.metadata.create_all(db_engine)

from src.core.logging import logger

logger.info(f'Database engine initialized using {db_url}')
