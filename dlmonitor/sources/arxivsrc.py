import os, sys
from ..db import create_engine
from .base import Source
from sqlalchemy_searchable import search
from sqlalchemy import desc
import feedparser
import time
from time import mktime
from datetime import datetime
import logging

SEARCH_KEY = "cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML"
MAX_QUERY_NUM = 10000

def mod_query_result(result):
    """
    Modify the query result to add required fields.
    """
    # Extract ArXiv URL from id
    result["arxiv_url"] = result["id"]
    
    # Extract PDF URL from links
    pdf_url = None
    for link in result.get("links", []):
        if link.get("type") == "application/pdf":
            pdf_url = link.get("href")
            break
    result["pdf_url"] = pdf_url or ""
    
    # Convert authors from list of dicts to list of strings
    authors_list = []
    for author in result.get("authors", []):
        if isinstance(author, dict) and "name" in author:
            authors_list.append(author["name"])
        elif isinstance(author, str):
            authors_list.append(author)
    result["authors"] = authors_list
    
    # Add journal reference from arxiv_comment if available
    result["journal_reference"] = result.get("arxiv_comment", "")

def prune_query_result(result):
    """
    Prune unnecessary fields from the query result.
    """
    # Keep only the fields we need for the database
    keep_fields = [
        "arxiv_url", "title", "summary", "pdf_url", "authors", 
        "updated_parsed", "journal_reference", "tags"
    ]
    
    # Remove fields we don't need
    keys_to_remove = [key for key in result.keys() if key not in keep_fields]
    for key in keys_to_remove:
        result.pop(key, None)

def query_arxiv(start=0, max_results=100):
    """
    Get papers from arxiv.
    """
    results = (feedparser.parse('https://export.arxiv.org/api/query?search_query=' + SEARCH_KEY +
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

    def get_one_post(self, arxiv_id):
        from ..db import session_scope, ArxivModel
        with session_scope() as session:
            query = session.query(ArxivModel).filter(ArxivModel.id == int(arxiv_id))
            results = query.all()
            if results:
                # Eagerly load all attributes to avoid DetachedInstanceError
                result = results[0]
                session.expunge(result)
                return result
            else:
                return None

    def get_posts(self, keywords=None, since=None, start=0, num=20):
        from ..db import session_scope, ArxivModel
        if keywords:
            keywords = keywords.strip()
        with session_scope() as session:
            query = session.query(ArxivModel)
            if since:
                # Filter date
                assert isinstance(since, str)
                query = query.filter(ArxivModel.published_time >= since)
            if not keywords or keywords.lower() == 'fresh papers':
                # Recent papers
                results = (query.order_by(desc(ArxivModel.published_time))
                           .offset(start).limit(num).all())
            elif keywords.lower() == 'hot papers':
                results = (query.order_by(desc(ArxivModel.popularity))
                                  .offset(start).limit(num).all())
            else:
                # search_kw = " or ".join(["({})".format(x) for x in keywords.split(",")])
                search_kw = " or ".join(keywords.split(","))
                searched_query = search(query, search_kw, sort=True)
                results = searched_query.offset(start).limit(num).all()

            # Expunge all results to avoid DetachedInstanceError
            for result in results:
                session.expunge(result)
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
