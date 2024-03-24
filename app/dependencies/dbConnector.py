from config.config import environ

from database.mysql import DB as mysql
from database.sqlite import DB as sqlite

from database.connector import dbConnector

def get_db_connector() -> dbConnector:
    connector = environ.connector
    if connector == 'sqlite':
        return sqlite()
    elif connector == 'mysql':
        return mysql()
    else:
        raise AttributeError(f'connector {connector} not available')