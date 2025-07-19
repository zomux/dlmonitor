# DLMonitor: Monitoring all things happening in deep learning

### Purpose

This project aims to save time and energy for deep learning folks.
It monitors new things on multiple sources and find out those important to you.
Currently, the data sources include:

- Arxiv papers
- Tweets
- Reddit posts

Take a look at the public server: https://deeplearn.org

### Install

1. Install postgres server
2. `pip install -r requirements.txt`
3. `sudo apt-get install poppler-utils`

### Setup database

1. Create a `.env` file in the project root.

```
DATABASE_USER=dlmonitor
DATABASE_PASSWD=something

TWITTER_CONSUMER_KEY=something
TWITTER_CONSUMER_SECRET=something
TWITTER_ACCESS_TOKEN=something
TWITTER_ACCESS_SECRET=something

SUPERVISORD_PASSWD=something
```

2. Create database

Run `bash bin/create_db.sh`


### Install Quick Read dependencies

1. install cpan
2. install text::Unidecode in cpan
3. git clone https://github.com/brucemiller/LaTeXML
4. perl Makefile.PL; make; make install

### Fetch resources

Fetch Arxiv papers and tweets.

```bash
python bin/fetch_new_sources.py all
```

### Run test server

```bash
PYTHONPATH="." python dlmonitor/webapp/app.py
```

### Setup production server

1. Install nginx

2. Copy configuration files for supervisord and nignx

```bash
bash bin/config_server.sh
```

3. Start Gunicorn processes through supervisord

```bash
bash bin/start_supervisord.sh
```
4. Start arxiv source loading worker

```bash
PYTHONPATH="." python bin/auto_load_arxiv.py --forever
```
