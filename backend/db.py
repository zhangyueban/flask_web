import sqlite3
from flask import g


database = 'data.sqlite'

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(database)
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def init_db():
    with open('db_init.sql', 'r', True, 'UTF-8') as f:
        init_sql = f.read()
    db = sqlite3.connect(database)
    db.executescript(init_sql)


if __name__ == '__main__':
    print('初始化数据库')
    init_db()