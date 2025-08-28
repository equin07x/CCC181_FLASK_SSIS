#To initialize the flask app
from flask import Flask, render_template, request, url_for, flash, redirect
import pymysql.cursors
from config import SECRET_KEY
from .database import db_connection


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    from .controller.students import students_bp
    app.register_blueprint(students_bp, url_prefix="/")
    
    from .controller.courses import courses_bp
    app.register_blueprint(courses_bp, url_prefix="/")
    
    from .controller.colleges import colleges_bp
    app.register_blueprint(colleges_bp, url_prefix="/")
    
    db = db_connection()
    cursor = db.cursor()
    def commit():
        db.commit()
        
       
    #This is for home when selecting which table to view
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')
  
    #Return function after the long def_create_app() function.
    return app