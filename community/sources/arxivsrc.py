import os, sys
from ..db import create_engine
from base import Source
from arxiv import mod_query_result, prune_query_result
from sqlalchemy_searchable import search
from sqlalchemy import desc
import feedparser
import time
from time import mktime
from datetime import datetime
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

    def get_posts(self, keywords=None, since=None, start=0, num=20):
        from ..db import get_global_session, ArxivModel
        session = get_global_session()
        query = session.query(ArxivModel)
        if since:
            # Filter date
            assert isinstance(since, str)
            query = query.filter(ArxivModel.published_time >= since)
        if not keywords or keywords.lower() == 'new papers':
            # Recent papers
            results = query.offset(start).limit(num).all()
        elif keywords.lower() == 'hot papers':
            results = (query.order_by(desc(ArxivModel.popularity))
                              .offset(start).limit(num).all())
        else:
            # search_kw = " or ".join(["({})".format(x) for x in keywords.split(",")])
            search_kw = " or ".join(keywords.split(","))
            searched_query = search(query, search_kw, sort=True)
            results = searched_query.offset(start).limit(num).all()
        return results

    def fetch_new(self):
        from ..db import session_scope, ArxivModel
        with session_scope() as session:
            for i in range(0, MAX_QUERY_NUM, 100):
                logging.info("get paper starting from {}".format(i))
                results = query_arxiv(start=i)
                anything_new = False
                for result in results:
                    arxiv_url = result["arxiv_url"]
                    if session.query(ArxivModel).filter_by(arxiv_url=arxiv_url).count() == 0:
                        anything_new = True
                        new_paper = ArxivModel(
                            arxiv_url=arxiv_url,
                            version=self._get_version(arxiv_url),
                            title=result["title"].replace("\n", "").replace("  ", " "),
                            abstract=result["summary"].replace("\n", "").replace("  ", " "),
                            pdf_url=result["pdf_url"],
                            authors=", ".join(result["authors"])[:800],
                            published_time=datetime.fromtimestamp(mktime(result["updated_parsed"])),
                            journal_link=result["journal_reference"],
                            tag=" | ".join([x["term"] for x in result["tags"]]),
                            popularity=0
                        )
                        session.add(new_paper)
                session.commit()
                if not anything_new:
                    break
                time.sleep(3)
