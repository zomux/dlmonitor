import os, sys
import re
from base import Source
from sqlalchemy_searchable import search
from sqlalchemy import desc
from ..settings import PROJECT_ROOT, TWITTER_ACCESS_TOKEN, TWITTER_CONSUMER_KEY, TWITTER_ACCESS_SECRET, TWITTER_CONSUMER_SECRET
import time
from time import mktime
from datetime import datetime
import logging
import twitter
from six.moves.html_parser import HTMLParser

TW_DATA_PATH = "{}/data/twitter_watching_list.txt".format(PROJECT_ROOT)

class TwitterSource(Source):

    def get_posts(self, keywords=None, since=None, start=0, num=30):
        from ..db import get_global_session, TwitterModel
        session = get_global_session()
        query = session.query(TwitterModel)
        if since:
            # Filter date
            assert isinstance(since, str)
            query = query.filter(TwitterModel.published_time >= since)
        if not keywords or keywords.lower() == 'fresh tweets':
            # Recent papers
            results = (query.order_by(desc(TwitterModel.published_time))
                       .offset(start).limit(num).all())
        elif keywords.lower() == 'hot tweets':
            results = (query.order_by(desc(TwitterModel.popularity))
                              .offset(start).limit(num).all())
        else:
            search_kw = " or ".join(keywords.split(","))
            searched_query = search(query, search_kw, sort=True)
            results = searched_query.offset(start).limit(num).all()

        # Unescape HTML
        parser = HTMLParser()
        for result in results:
            matches = re.findall(r"(https://t\.co/[^ .]{10})", result.text)
            result.href_text = result.text
            for match in matches:
                result.href_text = result.href_text.replace(match, '<a href="{}">{}</a>'.format(match, match))
        return results

    def _extract_arxiv_url(self, url):
        arxiv_url = url.replace("/pdf/", "/abs/")
        arxiv_url = arxiv_url.replace(".pdf", "")
        arxiv_url = arxiv_url.replace("https:", "http:")
        if "v" not in arxiv_url.split("/")[-1]:
            arxiv_url += "v1"
        return arxiv_url

    def fetch_new(self):
        from ..db import session_scope, TwitterModel, ArxivModel
        tw = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET,
                         access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_SECRET)
        with session_scope() as session:
            tw_watch_list = map(str.strip, open(TW_DATA_PATH).readlines())
            for tw_name in tw_watch_list:
                logging.info("get tweets from {}".format(tw_name))
                if tw_name.startswith("@"):
                    screen_name = tw_name.replace("@", "")
                    posts = tw.GetUserTimeline(screen_name=screen_name, count=200)
                else:
                    posts = tw.GetSearch(term=tw_name, result_type='mixed', count=200)
                for post in posts:
                    tweet_id = post.id_str
                    if session.query(TwitterModel).filter_by(tweet_id=tweet_id).count() == 0:
                        pic_url = None
                        if post.media:
                            for media in post.media:
                                if media.type == 'photo':
                                    pic_url = media.media_url_https
                                    break
                        new_tweet = TwitterModel(
                            tweet_id=tweet_id,
                            user=post.user.screen_name,
                            text=post.text,
                            published_time=post.created_at,
                            popularity=post.favorite_count,
                            pic_url=pic_url
                        )
                        session.add(new_tweet)
                        # Update arxiv paper popularity
                        for url in post.urls:
                            if "arxiv.org" in url.expanded_url:
                                arxiv_url = self._extract_arxiv_url(url.expanded_url)
                                affected_count = session.query(ArxivModel).filter_by(arxiv_url=arxiv_url).update(
                                    {"popularity": ArxivModel.popularity + 1 + post.favorite_count})
                                if affected_count == 0:
                                    print ("[WARN] Paper is not found: {}".format(arxiv_url))
                    else:
                        # Update popularity of this tweet and related arxiv post
                        tweet = session.query(TwitterModel).filter_by(tweet_id=tweet_id).first()
                        if tweet is not None:
                            if post.favorite_count > tweet.popularity:
                                tweet.popularity = post.favorite_count
                                for url in post.urls:
                                    if "arxiv.org" in url.expanded_url:
                                        arxiv_url = self._extract_arxiv_url(url.expanded_url)
                                        print ("Update popularity of {}".format(arxiv_url))
                                        paper = session.query(ArxivModel).filter_by(arxiv_url=arxiv_url).first()
                                        if paper:
                                            paper.popularity += post.favorite_count - tweet.popularity
                session.commit()
                time.sleep(1)
