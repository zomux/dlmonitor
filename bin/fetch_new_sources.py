import sys
sys.path.append(".")
from community.fetcher import fetch_sources
from argparse import ArgumentParser
import logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("src", help="source name: arxiv, twitter, youtube, reddit")
    args = ap.parse_args()

    fetch_sources(args.src)
