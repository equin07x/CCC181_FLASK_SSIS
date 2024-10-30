from flask import render_template, request, url_for, flash, redirect
from flask import Blueprint
from env import db

students_bp = Blueprint('sbp', __name__, template_folder="templates")

cursor = db.cursor()
def commit():
    db.commit()

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING STUDENTS STARTS IN HERE.#
#<-------------------------------------------------->#

@students_bp.route('/students')
def students():
    cursor.execute('SELECT * FROM course_table')
    courseCodes = cursor.fetchall()
    cursor.execute('SELECT * FROM students')
    data = cursor.fetchall()
    return render_template('/students/students.html', Students=data, Courses=courseCodes)

#For deleting a selected student
@students_bp.route('/delete_student/<string:students_id>', methods=["GET"])
def delete_student(students_id):
    print('The student has been successfully deleted!')
    flash("you have deleted a student information", category='secondary')
    cursor.execute("DELETE FROM students WHERE students_id = %s", (students_id))
    commit()
    return redirect(url_for('sbp.students'))

#For editing/updating the student information
@students_bp.route('/edit_student', methods=["POST"])
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
    return redirect(url_for('sbp.students'))


#For searching student information along with its selected fields
@students_bp.route('/students_results', methods=["POST"])
def student_search():
    cursor.execute('SELECT * FROM course_table')
    courseCodes = cursor.fetchall()
    if (request.method == "POST"):
        #GENERAL SEARCH
        student_key = request.form['student_key']
        course_key_Code = request.form['course_key_Code']
        student_key_Level = request.form['student_key_Level']
        student_key_Gender = request.form['student_key_Gender']

        
        if len(student_key) < 1:
            flash("You need to input a valid search", category='error')
            return (redirect(url_for('sbp.students')))
        
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
                return render_template('/students/student_results.html', student_key = search_data)      
        
        elif course_key_Code != "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
            print("This is state 2 of the student search results.")
            cursor.execute('''SELECT * FROM students WHERE
                            courseCode LIKE %s
                            AND firstName LIKE %s
                            OR courseCode LIKE %s AND lastName LIKE %s
                            OR idNumber LIKE %s''',(course_key_Code, student_key, course_key_Code, student_key, student_key)) 
            search_data = cursor.fetchall()
            return render_template('/students/student_results.html', student_key = search_data, Courses = courseCodes)
        
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
            return render_template('/students/student_results.html', student_key = search_data,  Courses = courseCodes)
        
        elif course_key_Code == "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender == "By Gender":
                print("This is state 4 of the student search results.")
                cursor.execute('''SELECT * FROM students WHERE
                                yearLevel LIKE %s AND
                                firstName LIKE %s OR yearLevel LIKE %s AND lastName LIKE %s''',
                                ( student_key_Level, student_key, student_key_Level, student_key)) 
                search_data = cursor.fetchall()
                return render_template('/students/student_results.html', student_key = search_data,  Courses = courseCodes)
            
        elif course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 5 of the student search results.")
            cursor.execute('''SELECT * FROM students WHERE
                            firstName LIKE %s AND gender LIKE %s
                            OR lastName LIKE %s AND gender LIKE %s''', 
                            ( student_key, student_key_Gender, student_key, student_key_Gender))
            search_data = cursor.fetchall()
            return render_template('/students/student_results.html', student_key = search_data, Courses = courseCodes)
        
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
            return render_template('/students/student_results.html', student_key = search_data,  Courses = courseCodes)
        
        elif course_key_Code != "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 7 of the student search results.")
            cursor.execute('''SELECT * FROM students WHERE firstName LIKE %s AND courseCode LIKE %s AND yearLevel LIKE %s AND gender LIKE %s
                            OR lastName LIKE %s AND courseCode LIKE %s AND yearLevel LIKE %s AND gender LIKE %s ''', 
                            (student_key, course_key_Code, student_key_Level, student_key_Gender,  
                                student_key, course_key_Code, student_key_Level, student_key_Gender))
            search_data = cursor.fetchall()
            return render_template('/students/student_results.html', student_key = search_data, Courses = courseCodes)
        
        elif course_key_Code != "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 8 of the student search results.")
            cursor.execute('''SELECT * FROM students WHERE
                            firstName LIKE %s AND courseCode LIKE %s AND gender LIKE %s
                            OR lastName LIKE %s AND courseCode LIKE %s AND gender LIKE %s''', 
                            ( student_key, course_key_Code, student_key_Gender, student_key, course_key_Code, student_key_Gender))
            search_data = cursor.fetchall()
            return render_template('/students/student_results.html', student_key = search_data, Courses = courseCodes)

#For adding a new student information
@students_bp.route('/add_students', methods=["POST"])
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

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING STUDENTS ENDS IN HERE.#
#<-------------------------------------------------->#
    