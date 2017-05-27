"""
A class for fetching all sources.
"""

from sources.arxivsrc import ArxivSource
from db import Base, engine

def get_source(src_name):
    if src_name == 'arxiv':
        return ArxivSource()
    else:
        raise NotImplementedError

def fetch_sources(src_name, fetch_all=False):
    global Base, engine
    Base.metadata.create_all(engine)
    src = get_source(src_name)
    if fetch_all:
        src.fetch_all()
    else:
        src.fetch_new()

def get_posts(src_name, keyword=None, start=0, num=100):
    src = get_source(src_name)
    return src.get_posts(keyword=keyword, start=start, num=num)
