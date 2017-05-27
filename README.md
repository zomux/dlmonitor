# Deep Community: All things happening in deep learning

### Install

1. Install mysql server
2. `pip install -r requirements.txt`

### Setup database

1. Create a `.env` file in the project root.

```
DATABASE_NAME=deepcommunity
DATABASE_USER=user
DATABASE_PASSWD=pass
```

2. Create database

Run `python bin/create_db.py`

### Fetch resources

Arxiv papers:

```bash
python bin/fetch_new_sources.py arxiv
```
