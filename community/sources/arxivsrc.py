import os, sys
from ..db import create_engine
from base import Source
from arxiv import mod_query_result, prune_query_result
import feedparser
import time
import logging

SEARCH_KEY = "cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML"
MAX_QUERY_NUM = 10000

def query_arxiv(start=0, max_results=100):
    """
    Get papers from arxiv.
    """
    results = (feedparser.parse('http://export.arxiv.org/api/query?search_query=' + SEARCH_KEY +
        '&sortBy=lastUpdatedDate&sortOrder=descending&start=' + str(start) + '&max_results=' + str(max_results)))
    if results.get('status') != 200:
        raise Exception("HTTP Error " + str(results.get('status', 'no status')) + " in query")
    else:
        results = results['entries']

    for result in results:
        mod_query_result(result)
        prune_query_result(result)
    return results


class ArxivSource(Source):

    def _get_version(self, arxiv_url):
        version = 1
        last_part = arxiv_url.split("/")[-1]
        if "v" in last_part:
            version = int(last_part.split("v")[-1])
        return version

    def fetch_new(self):
        from ..db import session_scope, ArxivModel
        with session_scope() as session:
            for i in range(0, 100, MAX_QUERY_NUM):
                results = query_arxiv(start=i)
                for result in results:
                    arxiv_url = result["arxiv_url"]
                    if session.query(ArxivModel).filter_by(arxiv_url=arxiv_url).count() == 0:
                        print result["title"].replace("\n", "")
                        print result["summary"].replace("\n", "")
                    print
                    # print result["pdf_url"]
                    # print ", ".join(result["authors"])
                    # print result["updated_parsed"]
                    # print result["journal_reference"]
                    # print " | ".join([x["term"] for x in result["tags"]])
                    break
                break
