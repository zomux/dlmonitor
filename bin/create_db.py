import os, sys
sys.path.append(".")
from community.settings import *

if __name__ == '__main__':
    os.system('echo "CREATE DATABASE {};" | mysql -u {} -p{} -h {}'.format(
        DATABASE_NAME, DATABASE_USER, DATABASE_PASSWD, DATABASE_ADDR
    ))
