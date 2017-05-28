import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


from . import settings
from db_models import Base, ArxivModel

def create_engine(**kwargs):
    return sqlalchemy.create_engine(settings.DATABASE_URL, **kwargs)

if 'Session' not in globals():
    engine = create_engine()
    sqlalchemy.orm.configure_mappers()
    Session = sessionmaker(bind=engine)

def get_global_session():
    global global_session
    if 'global_session' not in globals() or global_session is None:
        global_session = Session()
    return global_session

def close_global_session():
    global global_session
    global_session.close()
    global_session = None

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
