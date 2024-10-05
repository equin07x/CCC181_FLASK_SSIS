import pymysql

def db_connection():
    hostname = 'localhost'
    user = 'root'
    password = 'Antarisks159357'
    
    db = pymysql.connections.Connection(
        host=hostname,
        user=user,
        password=password
    )
    
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS flask_ssis')
    cursor.execute('SHOW DATABASES')
    
    for databases in cursor:
        print(databases)
        
    cursor.close()
    db.close()

db_connection()