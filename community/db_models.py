import sys
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

if 'Base' not in globals():
    Base = declarative_base()

def str_repr(string):
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

class ArxivModel(Base):

    __tablename__ = 'arxiv'

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer)
    title = Column(Unicode(800, collation='utf8_general_ci'))
    arxiv_url = Column(String(255), primary_key=True)
    pdf_url = Column(String(255))
    published_time = Column(DateTime())
    authors = Column(Unicode(800, collation='utf8_general_ci'))
    abstract = Column(Text(collation='utf8_general_ci'))
    journal_link = Column(String(255), nullable=True)
    tag = Column(String(255))

    def __repr__(self):
        template = '<Arxiv(id="{0}", url="{1}")>'
        return str_repr(template.format(self.id, self.arxiv_url))
