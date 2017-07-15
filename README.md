# Deep Community: All things happening in deep learning

### Install

1. Install postgres server
2. `pip install -r requirements.txt`
3. `sudo apt-get install poppler-utils`

### Setup database

1. Create a `.env` file in the project root.

```
DATABASE_USER=deepcommunity
DATABASE_PASSWD=something

TWITTER_CONSUMER_KEY=something
TWITTER_CONSUMER_SECRET=something
TWITTER_ACCESS_TOKEN=something
TWITTER_ACCESS_SECRET=something

SUPERVISORD_PASSWD=something
```

2. Create database

Run `bash bin/create_db.sh`

### Fetch resources

Fetch Arxiv papers and tweets.

```bash
python bin/fetch_new_sources.py all
```

### Setup web server

1. Install nginx

2. Copy configuration files for supervisord and nignx

```bash
bash bin/config_server.sh
```

2. Start Gunicorn processes through supervisord

```bash
bash bin/start_supervisord.sh
```
