import sys
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

if 'Base' not in globals():
    Base = declarative_base()
    make_searchable()

def str_repr(string):
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

class ArxivModel(Base):

    __tablename__ = 'arxiv'

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer)
    popularity = Column(Integer)
    title = Column(Unicode(800, collation=''))
    arxiv_url = Column(String(255), primary_key=True)
    pdf_url = Column(String(255))
    published_time = Column(DateTime())
    authors = Column(Unicode(800, collation=''))
    abstract = Column(Text(collation=''))
    journal_link = Column(Text(collation=''), nullable=True)
    tag = Column(String(255))

    # For full text search
    search_vector = Column(
        TSVectorType('title', 'abstract', 'authors', weights={'title': 'A', 'abstract': 'B', 'authors': 'C'}))

    def __repr__(self):
        template = '<Arxiv(id="{0}", url="{1}")>'
        return str_repr(template.format(self.id, self.arxiv_url))

class TwitterModel(Base):

    __tablename__ = 'twitter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(String(20), primary_key=True)
    popularity = Column(Integer)
    pic_url = Column(String(255), nullable=True)
    published_time = Column(DateTime())
    user = Column(Unicode(255))
    text = Column(Text())

    # For full text search
    search_vector = Column(TSVectorType('text'))

    def __repr__(self):
        template = '<Arxiv(id="{0}", user_name="{1}")>'
        return str_repr(template.format(self.id, self.user))
