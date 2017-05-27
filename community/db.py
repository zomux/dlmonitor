import sqlalchemy
from sqlalchemy.orm import sessionmaker

from . import settings

def create_engine(**kwargs):
    return sqlalchemy.create_engine(settings.DATABASE_URL, **kwargs)
