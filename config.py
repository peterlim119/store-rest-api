import sqlite3

global db_name

db_name = 'data.db'

class DBSQL:
    @classmethod
    def connection(self):
        conn = sqlite3.connect(db_name)
        return conn
