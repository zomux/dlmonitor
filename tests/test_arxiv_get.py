import sys
sys.path.append(".")
from community.sources.arxivsrc import ArxivSource
from community.db import close_global_session

if __name__ == '__main__':
    src = ArxivSource()
    for post in src.get_posts(num=5):
        print post.arxiv_url
        print post.title
    close_global_session()
