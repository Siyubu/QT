import os
from main import db

DB_NAME = "qtexam.db"
def create_database(app):
     if not os.path.exists('src/'+ DB_NAME):
        db.create_all(app = app)
        print("database created!!!")