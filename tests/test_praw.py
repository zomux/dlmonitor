import sys
sys.path.append(".")
from dlmonitor.settings import *
import praw

reddit = praw.Reddit(client_id='ognB0CMmO7EHRg',
                     client_secret='3G_pCLD9-m49Wk5A4Ut7wBHCIt8',
                     password='gx041136',
                     user_agent='dlmonitor',
                     username='zomux')
posts = reddit.subreddit("MachineLearning").search("Concrete Dropout")
for p in posts:
    import pdb;pdb.set_trace()
    print p
