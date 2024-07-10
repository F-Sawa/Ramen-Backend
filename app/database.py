import os
import mysql.connector
from flask import g #objeto que  actua como almacenamiento temporal
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'host' : os.getenv('BD_HOST'),
    'user' : os.getenv('BD_USUARIO'),
    'password' : os.getenv('BD_PASSW'),
    'database' : os.getenv('BD_NOMBRE'),
}

def getDB():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**DATABASE_CONFIG)
        except:
            g.db=None
            
    return g.db

def close_db(T):
    db= g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

