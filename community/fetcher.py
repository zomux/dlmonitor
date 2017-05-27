"""
A class for fetching all sources.
"""

from sources.arxivsrc import ArxivSource

def fetch_sources(src_name, fetch_all=False):
    src = None
    if src_name == 'arxiv':
        src = ArxivSource()
    else:
        raise NotImplementedError
    if fetch_all:
        src.fetch_all()
    else:
        src.fetch_new()
