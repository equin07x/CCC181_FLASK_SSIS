import pymysql
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
  
hostname = DB_HOST
user = DB_USERNAME
password = DB_PASSWORD
database = DB_NAME

def db_connection():
      db =  pymysql.connections.Connection(
        host=hostname,
        database=database,
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor)

      return db