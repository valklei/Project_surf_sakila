
import dotenv
import os
import sqlite3
from pymysql.cursors import DictCursor
def get_dbconfig():
    dotenv.load_dotenv()

    dbconfig = {
        'host': os.getenv('HOST'),
        'user': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
        'database': os.getenv('DATABASE')
    }

    return dbconfig
#


SQLITE_DB_PATH = 'search_keywords.db'
