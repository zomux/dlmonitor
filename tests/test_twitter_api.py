import sys
sys.path.append(".")
from community.settings import *
import twitter

tw = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET,
                 access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_SECRET)
# print 'q=%22Pre-Translation for Neural Machine Translation%22'
# print tw.GetSearch(term='#deeplearning', result_type = 'mixed', count=200)
# tw.GetUserTimeline(screen_name="deeplearninghub", count=200):
for post in tw.GetSearch(term='arxiv.org', result_type = 'mixed', count=200):
    print post.user.screen_name
    print post.created_at
    print post.id_str
    print post.favorite_count
    print post.text
    pic_url = None
    if post.media:
        for media in post.media:
            if media.type == 'photo':
                pic_url = media.media_url_https
                break
    for url in post.urls:
        print url.url, url.expanded_url
    print "---"
