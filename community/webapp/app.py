from flask import Flask, request
from flask import render_template, send_from_directory
from community.db import close_global_session
from community.fetcher import get_posts
from urllib2 import unquote

app = Flask(__name__, static_url_path='/static')

NUMBER_EACH_PAGE = 20

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/fetch', methods=['POST'])
def fetch():
    # Get keywords
    kw = request.cookies.get('keywords')
    if kw is not None:
        kw = unquote(kw)
    # Get parameters
    src = request.form.get("src")
    start = request.form.get("start")
    if src is None or start is None:
        # Error
        return ""
    assert "." not in src  # Just for security
    start = int(start)

    return render_template(
        "post_{}.html".format(src),
        posts=get_posts(src, keywords=kw, start=start, num=NUMBER_EACH_PAGE))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
