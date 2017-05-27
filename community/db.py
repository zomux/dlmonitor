import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from . import settings
from db_models import Base, ArxivModel

def create_engine(**kwargs):
    return sqlalchemy.create_engine(settings.DATABASE_URL, **kwargs)

if 'Session' not in globals():
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    global Session
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
