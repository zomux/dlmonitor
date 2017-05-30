import sys
sys.path.append(".")
from community.settings import *
import twitter

tw = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET,
                 access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_SECRET)
print 'q=%22Pre-Translation for Neural Machine Translation%22'
print tw.GetSearch(term='"Pre-Translation"', result_type = 'mixed', count=100, since="2016-01-01", until="2017-05-22")
