#To initialize the flask app
from flask import Flask, render_template, request, url_for, flash, redirect
import pymysql.cursors
from config import SECRET_KEY
from .database import db_connection


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    from .views.students import students_bp
    app.register_blueprint(students_bp, url_prefix="/")
    
    from .views.courses import courses_bp
    app.register_blueprint(courses_bp, url_prefix="/")
    
    db = db_connection()
    cursor = db.cursor()
    def commit():
        db.commit()
        
    cursor.execute('CREATE DATABASE IF NOT EXISTS flask_ssis')
    cursor.execute('SHOW DATABASES')
     
    if cursor.execute('CREATE DATABASE IF NOT EXISTS flask_ssis'):
        print("Database Connected!")
        
    #This is for home when selecting which table to view
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('home.html')
  
    
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING COLLEGES STARTS IN HERE.#
    #<-------------------------------------------------->#
    
    #This is for accessing college table and its actions:
    @app.route('/colleges')
    def colleges():
        cursor.execute("SELECT * FROM college_table")
        data = cursor.fetchall()
        return render_template('/colleges/colleges.html', College=data)
    
    #For editing a college information
    @app.route('/edit_college', methods=["GET","POST"])
    def edit_college():
        if request.method == "POST":
            print('successfully edited the select item')
            college_id = request.form['college_id']
            collegeCodeEdit = request.form['collegeCodeEdit']
            collegeNameEdit = request.form['collegeNameEdit']
            
            if len(collegeCodeEdit) < 1:
                flash("You have to input a valid college!", category="error")
            elif len(collegeNameEdit) < 1:
                flash("You have to input a valid college!", category="error")
            else:
                flash("You have successfuly edited a college!", category="success")
                cursor.execute("UPDATE college_table SET collegeCode=%s, collegeName=%s WHERE college_id=%s", 
                           (collegeCodeEdit, collegeNameEdit, college_id))
                commit()
        return redirect(url_for('colleges'))
    
    #For searching an input for college_table
    @app.route('/college_search', methods=["POST"])
    def college_search():
        if (request.method == "POST"):
            #GENERAL SEARCH
            college_key = request.form['college_key']
            
            if len(college_key) < 1:
                flash("You need to input a valid search", category='error')
                return (redirect(url_for('colleges')))
            elif request.form['college_key_Code'] == "By College Code" and request.form['college_key_Name'] == "By College Name":
                print("This is route 1")
                cursor.execute('''SELECT * FROM college_table WHERE collegeCode LIKE %s OR collegeName LIKE %s''', 
                            (college_key, college_key))
                search_data = cursor.fetchall()
                return render_template('college_results.html', college_key = search_data)
            
            #THIS IS FOR SEARCHING COLLEGE CODE WITH EXCLUSIVITY
            elif request.form['college_key_Code'] != "By College Code" and request.form['college_key_Name'] == "By College Name":
                print("This is route 2")
                college_key = request.form['college_key']
                college_key_Code = request.form['college_key_Code']
                cursor.execute('''SELECT * FROM college_table WHERE collegeCode LIKE %s AND collegeName LIKE %s''', 
                            (college_key_Code, college_key))
                search_data = cursor.fetchall()
                return render_template('college_results.html', college_key = search_data)
            
            #THIS IS FOR SEARCHING COLLEGE NAME FIELDS WITH EXCLUSIVITY
            elif request.form['college_key_Code'] == "By College Code" and request.form['college_key_Name'] != "By College Name":
                print("This is route 3")
                college_key = request.form['college_key']
                college_key_Name = request.form['college_key_Name']
                cursor.execute('''SELECT * FROM college_table WHERE collegeName LIKE %s AND collegeCode LIKE %s''', 
                            (college_key_Name, college_key))
                search_data = cursor.fetchall()
                return render_template('college_results.html', college_key = search_data)
            
            #THIS IS FOR SEARCH COLLEGE CODE AND COLLEGE NAME FIELDS WITH EXCLUSIVITY
            elif request.form['college_key_Code'] != "By College Code" and request.form['college_key_Name'] != "By College Name":
                print("This is route 4")
                college_key = request.form['college_key']
                college_key_Name = request.form['college_key_Name']
                college_key_Code = request.form['college_key_Code']
                cursor.execute('''SELECT * FROM college_table WHERE collegeName LIKE %s AND collegeCode LIKE %s''', 
                            (college_key_Name, college_key_Code))
                search_data = cursor.fetchall()
                return render_template('college_results.html', college_key = search_data)
            else:
                return render_template('college_results.html')
        
    #For deleting a selected college item
    @app.route('/delete_college/<string:collegeCode>', methods=["GET"])
    def delete_college(collegeCode):
        print('The college has been successfully deleted!')
        cursor.execute("DELETE FROM college_table WHERE collegeCode = %s", (collegeCode))
        cursor.execute("UPDATE course_table SET collegeCode = 'N/A' WHERE collegeCode = %s", (collegeCode))
        flash("You have deleted college information. It will take effect on the courses under the deleted. ", category='secondary')
        commit()
        return redirect(url_for('colleges'))
    
    #For adding a new college information
    @app.route('/add_college', methods=["GET", "POST"])
    def add_college():
        if request.method == "POST":
            collegeCode = request.form['collegeCode']
            collegeName = request.form['collegeName']
            
            if len(collegeCode) < 1:
                flash("You have to input a valid college!", category="error")
            elif len(collegeName) < 1:
                flash("You have to input a valid college!", category="error")
            else:
                cursor.execute("INSERT INTO college_table(collegeCode, collegeName) VALUES (%s, %s)", (collegeCode, collegeName))
                flash("You have successfuly added college!", category="success")
                commit()
        return redirect(url_for('colleges'))
    
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING COLLEGES ENDS IN HERE.#
    #<-------------------------------------------------->#
    
    #Return function after the long def_create_app() function.
    return app