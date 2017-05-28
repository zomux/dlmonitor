from flask import Flask
from flask import render_template, send_from_directory
from community.db import close_global_session
from community.fetcher import get_posts

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template("index.html", posts=get_posts('arxiv', num=20))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
