import sqlite3
from config import DBSQL
from resources.item import ItemRes
from models.item import ItemModel

# db_name = config.db_name

def create_userTable():
    conn = DBSQL.connection()    #sqlite3.connect(db_name)
    cursor = conn.cursor()
    sqlCreate = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
    cursor.execute(sqlCreate)
    conn.commit()
    conn.close()

def create_itemTable():
    conn = DBSQL.connection()    #sqlite3.connect(db_name)
    # conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sqlCreate = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY,name text, price real)"
    cursor.execute(sqlCreate)

    # cursor.execute("insert into items values(NULL, 'book',200)")
    # cursor.execute("insert into items values(NULL, 'pen',15.40)")
    # cursor.execute("insert into items values(NULL, 'chair',150.99)")

    conn.commit()
    conn.close()


create_userTable()
create_itemTable()

# myitem = ItemModel('chair',12.03)
# print(myitem.json())
#
# #myitem.add_item('kiss',200.345)
# myItemRes = ItemRes()
# print(myItemRes.get('book'))
# print(myitem.get_items())

