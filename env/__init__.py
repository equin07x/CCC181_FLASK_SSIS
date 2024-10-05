#To initialize the flask app
from flask import Flask, render_template, request, url_for, flash, redirect
import pymysql.cursors
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
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
    #THE CODES RELATED FOR HANDLING STUDENTS STARTS IN HERE.#
    #<-------------------------------------------------->#
    
    #This is for accessing students table and its actions:
    @app.route('/students')
    def students():
        cursor.execute('SELECT * FROM course_table')
        courseCodes = cursor.fetchall()
        cursor.execute('SELECT * FROM students')
        data = cursor.fetchall()
        return render_template('students.html', Students=data, Courses=courseCodes)
    
    #For searching student information along with its selected fields
    @app.route('/student_search', methods=["POST"])
    def student_search():
        if (request.method == "POST"):
            #GENERAL SEARCH
            student_key = request.form['student_key']
            course_key_Code = request.form['course_key_Code']
            student_key_Level = request.form['student_key_Level']
            student_key_Gender = request.form['student_key_Gender']

            
            if len(student_key) < 1:
                flash("You need to input a valid search", category='error')
                return (redirect(url_for('students')))
            
            elif course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
                    print("This is state 1 of the student search results.")
                    cursor.execute('''SELECT * FROM students WHERE idNumber LIKE %s 
                                    OR firstName LIKE %s
                                    OR lastName LIKE %s
                                    OR courseCode LIKE %s
                                    OR yearLevel LIKE %s
                                    OR gender LIKE %s''', 
                                    (student_key, student_key, student_key, 
                                        student_key, student_key, student_key))
                    search_data = cursor.fetchall()
                    return render_template('student_results.html', student_key = search_data)      
            
            elif course_key_Code != "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
                print("This is state 2 of the student search results.")
                cursor.execute('''SELECT * FROM students WHERE
                                courseCode LIKE %s
                                AND firstName LIKE %s
                                OR courseCode LIKE %s AND lastName LIKE %s
                                OR idNumber LIKE %s''',(course_key_Code, student_key, course_key_Code, student_key, student_key)) 
                search_data = cursor.fetchall()
                return render_template('student_results.html', student_key = search_data)
            
            elif course_key_Code != "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender == "By Gender":
                print("This is state 3 of the student search results.")
                cursor.execute('''SELECT * FROM students WHERE
                                courseCode LIKE %s AND yearLevel LIKE %s 
                                AND firstName LIKE %s
                                OR courseCode LIKE %s AND yearLevel LIKE %s AND
                                lastName LIKE %s OR idNumber LIKE %s''',
                                (course_key_Code, student_key_Level, student_key, 
                                 course_key_Code, student_key_Level, student_key, student_key)) 
                search_data = cursor.fetchall()
                return render_template('student_results.html', student_key = search_data)
            
            elif course_key_Code == "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender == "By Gender":
                    print("This is state 4 of the student search results.")
                    cursor.execute('''SELECT * FROM students WHERE
                                    yearLevel LIKE %s AND
                                    firstName LIKE %s OR yearLevel LIKE %s AND lastName LIKE %s''',
                                    ( student_key_Level, student_key, student_key_Level, student_key)) 
                    search_data = cursor.fetchall()
                    return render_template('student_results.html', student_key = search_data)
                
            elif course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender != "By Gender":
                print("This is state 5 of the student search results.")
                cursor.execute('''SELECT * FROM students WHERE
                                firstName LIKE %s AND gender LIKE %s
                                OR lastName LIKE %s AND gender LIKE %s''', 
                                ( student_key, student_key_Gender, student_key, student_key_Gender))
                search_data = cursor.fetchall()
                return render_template('student_results.html', student_key = search_data)
            
            elif course_key_Code == "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender != "By Gender":
                print("This is state 6 of the student search results.")
                cursor.execute('''SELECT * FROM students WHERE 
                                 yearLevel LIKE %s 
                                    AND gender LIKE %s 
                                    AND firstName LIKE %s
                                OR  yearLevel LIKE %s 
                                    AND gender LIKE %s 
                                    AND lastName LIKE %s''', 
                                (student_key_Level, student_key_Gender, student_key, student_key_Level, student_key_Gender, 
                                    student_key))
                search_data = cursor.fetchall()
                return render_template('student_results.html', student_key = search_data)
            
            elif course_key_Code != "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender != "By Gender":
                print("This is state 7 of the student search results.")
                cursor.execute('''SELECT * FROM students WHERE firstName LIKE %s AND courseCode LIKE %s AND yearLevel LIKE %s AND gender LIKE %s
                                OR lastName LIKE %s AND courseCode LIKE %s AND yearLevel LIKE %s AND gender LIKE %s ''', 
                                (student_key, course_key_Code, student_key_Level, student_key_Gender,  
                                 student_key, course_key_Code, student_key_Level, student_key_Gender))
                search_data = cursor.fetchall()
                return render_template('student_results.html', student_key = search_data)

    #For editing/updating the student information
    @app.route('/edit_student', methods=["POST"])
    def edit_students():
        if request.method == "POST":
            print('successfully edited the select item')
            student_id = request.form['student_id']
            idNumberEdit = request.form['idNumberEdit']
            firstNameEdit = request.form['firstNameEdit']
            lastNameEdit =  request.form['lastNameEdit']
            courseCodeEdit = request.form['courseCodeEdit']
            yearLevelEdit = request.form['yearLevelEdit']
            genderEdit = request.form['genderEdit']
            
            if len(idNumberEdit) < 6:
                flash("You need to input valid ID Number!", category='error')
            elif len(firstNameEdit) < 2:
                flash("You need to input valid first name!", category='error')
            elif len(lastNameEdit) < 2:
                flash("You need to input valid last name!", category='error')    
            else:    
                cursor.execute('''UPDATE students SET idNumber=%s, firstName=%s, lastName=%s, 
                            courseCode=%s, yearLevel=%s, gender=%s WHERE students_id=%s''', 
                            (idNumberEdit, firstNameEdit, lastNameEdit, 
                                courseCodeEdit, yearLevelEdit, genderEdit, student_id))
                commit()
                flash("you have successfully edited the student information!", category='success')
        return redirect(url_for('students'))
    
    #For adding a new student information
    @app.route('/add_students', methods=["POST"])
    def add_student():
        if request.method == "POST": 
            idNumber = request.form['idNumber']
            firstName = request.form['firstName']
            lastName =  request.form['lastName']
            courseCode = request.form['courseCode']
            yearLevel = request.form['yearLevel']
            gender = request.form['gender']
            
            if len(idNumber) < 1:
                flash("You need to input valid ID Number!", category='error')
            elif len(firstName) < 1:
                flash("You need to input valid first name!", category='error')
            elif len(lastName) < 1:
                flash("You need to input valid last name!", category='error')    
            else:
                cursor.execute('''INSERT INTO students(idNumber, firstName, 
                lastName, courseCode, yearLevel, gender) VALUES (%s, %s, %s, %s, %s, %s)''', 
                            (idNumber, firstName, lastName, 
                                    courseCode, yearLevel, gender))
                commit()
                flash("Successfully added the student information!", category='success')
                print("You have successfully added a student")
        return redirect(url_for('students'))
    
    #For deleting a selected student
    @app.route('/delete_student/<string:students_id>', methods=["GET"])
    def delete_student(students_id):
        print('The student has been successfully deleted!')
        flash("you have deleted a student information", category='secondary')
        cursor.execute("DELETE FROM students WHERE students_id = %s", (students_id))
        commit()
        return redirect(url_for('students'))
    
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING STUDENTS ENDS IN HERE.#
    #<-------------------------------------------------->#
       
    
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING COURSES STARTS IN HERE.#
    #<-------------------------------------------------->#
    
    #This is for accessing courses table and its actions:
    @app.route('/courses')
    def courses():
        cursor.execute("SELECT * FROM course_table")
        course_data = cursor.fetchall()
        cursor.execute("SELECT * FROM college_table")
        college_data = cursor.fetchall()
        return render_template('courses.html', Courses=course_data, Colleges=college_data)
    
    #For editing/updating the course information
    @app.route('/edit_course', methods = ["POST"])
    def edit_course():
        if request.method == "POST":
            print('successfully edited the select item')
            course_id = request.form['course_id']
            courseCodeEdit = request.form['courseCodeEdit']
            courseNameEdit = request.form['courseNameEdit']
            collegeCodeEdit =  request.form['collegeCodeEdit']
            cursor.execute("SELECT * FROM course_table WHERE course_id=%s", (course_id))
            data = cursor.fetchall()
            print(data)
            
            if len(courseCodeEdit) < 1:
                flash("You need to input valid course code!", category='error')
            elif len(courseNameEdit) < 1:
                flash("You need to input valid course name!", category='error') 
            else:
                cursor.execute("UPDATE course_table SET courseCode=%s, courseName=%s, collegeCode=%s WHERE course_id=%s", 
                            (courseCodeEdit, courseNameEdit, collegeCodeEdit, course_id))
                flash("you have successfully edited the course information!", category='success')
                commit()
        return redirect(url_for('courses'))
    
    #For adding a new course information
    @app.route('/add_course', methods=["GET","POST"])
    def add_course():
        if request.method == "POST":
            courseCode = request.form['courseCode']
            courseName = request.form['courseName']
            collegeCode = request.form['collegeCode']
            
            if len(courseCode) < 1:
                flash("You need to input valid course code!", category='error')
            elif len(courseName) < 1:
                flash("You need to input valid course name!", category='error') 
            else:
                cursor.execute("INSERT INTO course_table( courseCode, courseName, collegeCode) VALUES (%s, %s, %s)", 
                            (courseCode, courseName, collegeCode))
                flash("Successfully added the course information!", category="success")
                commit()
        return redirect(url_for('courses'))
    
    #For deleting courses
    @app.route('/delete_course/<string:courseCode>', methods=["GET"])
    def delete_course(courseCode):
        print('The course has been successfully deleted!')
        cursor.execute("DELETE FROM course_table WHERE courseCode = %s", (courseCode))
        cursor.execute("UPDATE students SET courseCode = 'N/A' WHERE courseCode = %s", (courseCode))
        flash("You have deleted course information. It will take effect on the students enrolled on the deleted course. ", category='secondary')
        commit()
        return redirect(url_for('courses'))
    
    #For searching courses
    @app.route('/course_search', methods=["POST"])
    def course_search():
        if (request.method == "POST"):
            #GENERAL SEARCH
            course_key = request.form['course_key']
            course_key_Code = request.form['course_key_Code']
            course_key_Name = request.form['course_key_Name']
            college_key_Code = request.form['college_key_Code']
            
            if len(course_key) < 1:
                flash("You need to input a valid search", category='error')
                return (redirect(url_for('courses')))
            elif course_key_Code == "By Course Code" and course_key_Name == "By Course Name" and college_key_Code == "By College Code":
                print("This is state 1 for searching courses")
                cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s OR courseName LIKE %s OR collegeCode LIKE %s''', 
                            (course_key, course_key, course_key))
                search_data = cursor.fetchall()
                return render_template('course_results.html', course_key = search_data)
            
            #THIS IS FOR SEARCHING COURSES CODE WITH EXCLUSIVITY
            elif course_key_Code != "By Course Code" and course_key_Name == "By Course Name" and college_key_Code == "By College Code":
                print("This is state 2 for searching courses")
                cursor.execute('''SELECT * FROM course_table WHERE courseName LIKE %s OR collegeCode LIKE %s AND courseCode LIKE %s ''', 
                            (course_key, course_key, course_key_Code))
                search_data = cursor.fetchall()
                return render_template('course_results.html', course_key = search_data)
            
            #THIS IS FOR SEARCHING COURSES NAME WITH EXCLUSIVITY
            elif course_key_Code == "By Course Code" and course_key_Name != "By Course Name" and college_key_Code == "By College Code":
                print("This is state 3 for searching courses")
                cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  OR collegeCode LIKE %s AND courseName LIKE %s ''', 
                            (course_key, course_key, course_key_Name))
                search_data = cursor.fetchall()
                return render_template('course_results.html', course_key = search_data)
            
            
            #THIS IS FOR SEARCHING COLLEGE CODE FIELDS WITH EXCLUSIVITY
            elif course_key_Code == "By Course Code" and course_key_Name == "By Course Name" and college_key_Code != "By College Code":
                print("This is state 4 for searching courses")
                cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  OR courseName LIKE %s AND collegeCode LIKE %s''', 
                            (course_key, course_key, college_key_Code))
                search_data = cursor.fetchall()
                return render_template('course_results.html', course_key = search_data)
            
            #THIS IS FOR SEARCHING FIELDS WITH EXCLUSIVITY
            elif course_key_Code != "By Course Code" and course_key_Name != "By Course Name" and college_key_Code != "By College Code":
                print("This is state 5 for searching courses")
                cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  AND courseName LIKE %s AND collegeCode LIKE %s''', 
                            (course_key_Code, course_key_Name, college_key_Code))
                search_data = cursor.fetchall()
                return render_template('course_results.html', course_key = search_data)
            
            else:
                return render_template('college_results.html')
   
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING COURSES ENDS IN HERE.#
    #<-------------------------------------------------->#
    
    
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING COLLEGES STARTS IN HERE.#
    #<-------------------------------------------------->#
    
    #This is for accessing college table and its actions:
    @app.route('/colleges')
    def colleges():
        cursor.execute("SELECT * FROM college_table")
        data = cursor.fetchall()
        return render_template('colleges.html', College=data)
    
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