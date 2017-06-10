from flask import Flask, request
from flask import render_template, send_from_directory
from community.db import close_global_session
from community.fetcher import get_posts
from urllib2 import unquote
import datetime as DT

app = Flask(__name__, static_url_path='/static')

NUMBER_EACH_PAGE = 30
DEFAULT_KEYWORDS = "Hot Tweets,Fresh Tweets,Hot Papers,Fresh Papers"

DATE_TOKEN_SET = set(['1-week', '2-week', '1-month'])

def get_date_str(token):
    """
    Convert token to date string.
    For example, '1-week' ---> '2017-04-03'.
    """
    today = DT.date.today()
    if token not in DATE_TOKEN_SET:
        token = '2-week'
    if token == '1-week':
        target_date = today - DT.timedelta(days=7)
    elif token == '2-week':
        target_date = today - DT.timedelta(days=14)
    else:
        target_date = today - DT.timedelta(days=31)
    return target_date.strftime("%Y-%m-%d")

@app.route('/')
def index():
    keywords = request.cookies.get('keywords')
    if not keywords:
        keywords = DEFAULT_KEYWORDS
    else:
        keywords = unquote(keywords)
    target_date = get_date_str(request.cookies.get('datetoken'))
    column_list = []
    for kw in keywords.split(","):
        src = "twitter" if "tweets" in kw.lower() else "arxiv"
        num_page = 80 if src == "twitter" else NUMBER_EACH_PAGE
        posts = get_posts(src, keywords=kw, since=target_date, start=0, num=num_page)
        column_list.append((src, kw, posts))

    return render_template("index.html", columns=column_list)

@app.route('/fetch', methods=['POST'])
def fetch():
    # Get keywords
    kw = request.form.get('keyword')
    if kw is not None:
        kw = unquote(kw)
    # Get parameters
    src = request.form.get("src")
    start = request.form.get("start")
    if src is None or start is None:
        # Error if 'src' or 'start' parameter is not found
        return ""
    assert "." not in src  # Just for security
    start = int(start)
    # Get target date string
    target_date = get_date_str(request.cookies.get('datetoken'))

    num_page = 80 if src == "twitter" else NUMBER_EACH_PAGE

    return render_template(
        "post_{}.html".format(src),
        posts=get_posts(src, keywords=kw, since=target_date, start=start, num=num_page))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
