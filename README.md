# Deep Community: All things happening in deep learning

### Install

1. Install postgres server
2. `pip install -r requirements.txt`

### Setup database

1. Create a `.env` file in the project root.

```
DATABASE_NAME=deepcommunity
DATABASE_USER=user
DATABASE_PASSWD=pass
```

2. Create database

Run `bash bin/create_db.sh`

### Fetch resources

Fetch Arxiv papers:

```bash
python bin/fetch_new_sources.py arxiv
```

### Setup web server

1. Copy configuration files for supervisord and nignx

```bash
bash bin/config_server.sh
```

2. Start Gunicorn processes through supervisord

```bash
bash bin/start_supervisord.sh
```
