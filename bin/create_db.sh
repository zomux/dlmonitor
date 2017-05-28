source ./.env
sudo -u postgres psql -c "create user $DATABASE_USER createdb createuser password
'$DATABASE_PASSWD';"
sudo -u postgres psql -c "create database deepcommunity owner $DATABASE_USER;"
