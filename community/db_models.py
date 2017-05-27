from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import create_engine

Base = declarative_base()

def print_schema():
    engine = create_engine(echo=True)
    print Base.metadata.create_all(engine)

def str_repr(string):
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

class Arxiv(Base):

    __tablename__ = 'arxiv'

    id = Column(Integer, primary_key=True)
    title = Column(String(800))
    arxiv_url = Column(String(255))
    pdf_url = Column(String(255))
    published_time = Column(DateTime())
    authors = Column(String(800))
    abstract = Column(Text())
    journal_link = Column(String(255))

    def __repr__(self):
        template = '<Arxiv(id="{0}", name="{1}")>'
        return str_repr(template.format(self.id, self.arxiv_url))
