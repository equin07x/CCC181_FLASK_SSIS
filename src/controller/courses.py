from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
import pymysql.cursors
from config import SECRET_KEY
from src.database import db_connection
from models.courses import course_M
#from models.students import student_M



courses_bp = Blueprint("Cbp", __name__,  template_folder='/templates')


#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COURSES STARTS IN HERE.#
#<-------------------------------------------------->#

#This is for accessing courses table and its actions:
@courses_bp.route('/courses')
def courses():
    course_data = course_M.display_Courses()
    college_data = course_M.display_Colleges()
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
        
        if len(courseCodeEdit) < 1:
            flash("You need to input valid course code!", category='error')
        elif len(courseNameEdit) < 1:
            flash("You need to input valid course name!", category='error') 
        else:
            course_M.edit_Course(courseCodeEdit, courseNameEdit, collegeCodeEdit, course_id)
            flash("you have successfully edited the course information!", category='success')
    return redirect(url_for('Cbp.courses'))

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
            course_M.add_Course(courseCode, courseName, collegeCode)
            flash("Successfully added the course information!", category="success")
    return redirect(url_for('Cbp.courses'))

#For deleting courses
@courses_bp.route('/delete_course/<string:courseCode>', methods=["GET"])
def delete_course(courseCode):
    print('The course has been successfully deleted!')
    course_M.delete_Course(courseCode)
    flash("You have deleted course information. It will take effect on the students enrolled on the deleted course. ", category='secondary')
    return redirect(url_for('Cbp.courses'))

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
            return (redirect(url_for('Cbp.courses')))
        elif len(course_key) > 1:
            search_data = course_M.search_Course(course_key, course_key_Name, course_key_Code, college_key_Code)
            return render_template('/courses/course_results.html', course_key = search_data)
        else:
            return render_template('/courses/courses.html')

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COURSES ENDS IN HERE.#
#<-------------------------------------------------->#


