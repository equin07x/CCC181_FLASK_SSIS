#To initialize the flask app
from flask import Flask, render_template
import pymysql.cursors
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY


hostname = DB_HOST
user = DB_USERNAME
password = DB_PASSWORD
database = DB_NAME

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    database = database
)

cursor = db.cursor()
def commit():
    db.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    #importing the students module
    from .students.sbp import students_bp
    app.register_blueprint(students_bp, url_prefix="/")
    #importing the courses module
    from .courses.cbp import courses_bp
    app.register_blueprint(courses_bp, url_prefix="/")
    #importing the colleges module
    from .colleges.clbp import colleges_bp
    app.register_blueprint(colleges_bp, url_prefix="/")
        
    cursor.execute('CREATE DATABASE IF NOT EXISTS flask_ssis')
    cursor.execute('SHOW DATABASES')
     
    if cursor.execute('CREATE DATABASE IF NOT EXISTS flask_ssis'):
        print("Database Connected!")
    
    
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')
    
    @app.route('/colleges')
    def colleges():
        cursor.execute("SELECT * FROM college_table")
        data = cursor.fetchall()
        return render_template('/colleges/colleges.html', College=data)

   
    #Return function after the long def_create_app() function.
    return app