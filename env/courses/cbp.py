from flask import render_template, request, url_for, flash, redirect
from flask import Blueprint
from env import db


courses_bp = Blueprint('cbp', __name__, template_folder="templates")

cursor = db.cursor()
def commit():
    db.commit()

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COURSES STARTS IN HERE.#
#<-------------------------------------------------->#

#This is for accessing courses table and its actions: 

@courses_bp.route('/courses')
def courses():
    cursor.execute("SELECT * FROM course_table")
    course_data = cursor.fetchall()
    cursor.execute("SELECT * FROM college_table")
    college_data = cursor.fetchall()
    return render_template('/courses/courses.html', Courses=course_data, Colleges=college_data)

#For editing/updating the course information
@courses_bp.route('/edit_course', methods = ["POST"])
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
    return redirect(url_for('cbp.courses'))

#For adding a new course information
@courses_bp.route('/add_course', methods=["GET","POST"])
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
    return redirect(url_for('cbp.courses'))

#For deleting courses
@courses_bp.route('/delete_course/<string:courseCode>', methods=["GET"])
def delete_course(courseCode):
    print('The course has been successfully deleted!')
    cursor.execute("DELETE FROM course_table WHERE courseCode = %s", (courseCode))
    cursor.execute("UPDATE students SET courseCode = 'N/A' WHERE courseCode = %s", (courseCode))
    flash("You have deleted course information. It will take effect on the students enrolled on the deleted course. ", category='secondary')
    commit()
    return redirect(url_for('cbp.courses'))

#For searching courses
@courses_bp.route('/course_search', methods=["POST"])
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
            return render_template('/courses/course_results.html', course_key = search_data)
        
        #THIS IS FOR SEARCHING COURSES CODE WITH EXCLUSIVITY
        elif course_key_Code != "By Course Code" and course_key_Name == "By Course Name" and college_key_Code == "By College Code":
            print("This is state 2 for searching courses")
            cursor.execute('''SELECT * FROM course_table WHERE courseName LIKE %s OR collegeCode LIKE %s AND courseCode LIKE %s ''', 
                        (course_key, course_key, course_key_Code))
            search_data = cursor.fetchall()
            return render_template('/courses/course_results.html', course_key = search_data)
        
        #THIS IS FOR SEARCHING COURSES NAME WITH EXCLUSIVITY
        elif course_key_Code == "By Course Code" and course_key_Name != "By Course Name" and college_key_Code == "By College Code":
            print("This is state 3 for searching courses")
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  OR collegeCode LIKE %s AND courseName LIKE %s ''', 
                        (course_key, course_key, course_key_Name))
            search_data = cursor.fetchall()
            return render_template('/courses/course_results.html', course_key = search_data)
        
        
        #THIS IS FOR SEARCHING COLLEGE CODE FIELDS WITH EXCLUSIVITY
        elif course_key_Code == "By Course Code" and course_key_Name == "By Course Name" and college_key_Code != "By College Code":
            print("This is state 4 for searching courses")
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  OR courseName LIKE %s AND collegeCode LIKE %s''', 
                        (course_key, course_key, college_key_Code))
            search_data = cursor.fetchall()
            return render_template('/courses/course_results.html', course_key = search_data)
        
        #THIS IS FOR SEARCHING FIELDS WITH EXCLUSIVITY
        elif course_key_Code != "By Course Code" and course_key_Name != "By Course Name" and college_key_Code != "By College Code":
            print("This is state 5 for searching courses")
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  AND courseName LIKE %s AND collegeCode LIKE %s''', 
                        (course_key_Code, course_key_Name, college_key_Code))
            search_data = cursor.fetchall()
            return render_template('/courses/course_results.html', course_key = search_data)
        
        else:
            return render_template('/courses/course_results.html')

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COURSES ENDS IN HERE.#
#<-------------------------------------------------->#