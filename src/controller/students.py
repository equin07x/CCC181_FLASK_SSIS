from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
import pymysql.cursors
from config import SECRET_KEY
from src.database import db_connection
from models.students import student_M



students_bp = Blueprint("Sbp", __name__,  template_folder='/templates')

  
    #<-------------------------------------------------->#
    #THE CODES RELATED FOR HANDLING STUDENTS STARTS IN HERE.#
    #<-------------------------------------------------->#
    
    #This is for accessing students table and its actions:
@students_bp.route('/students')
def students():
    #displays all of the students
    students = student_M.display_Students()

    # 2.) IMPLEMENT A DYNAMIC PAGINATION ON SEARCH
    # 3.) THE SEARCH SHOULD SHOW THE COURSE NAME ALONG SIDE THE COLLEGE CODE IN THIS FORMAT: <COURSE_CODE>(<COURSE_NAME>)
    page = request.args.get('page', 1, type=int)
    print(page)
    per_Page = 10
    start_Page = (page - 1) * per_Page
    end_Page = start_Page + per_Page
    
    students_on_Page = students[start_Page:end_Page]

    total_Pages = len(students_on_Page) + per_Page - 1 // per_Page
    print(total_Pages)
    page_Number = list(range(1, total_Pages))
    print(page_Number)
    
    #displays all of the courses
    courses = student_M.display_Courses()
    
    return render_template('/students/students.html', Students=students_on_Page, Courses=courses,
                           page = page, number_of_Pages = page_Number, total_Pages = total_Pages)

#For searching student information along with its selected fields
@students_bp.route('/student_search', methods=["POST"])
def student_search():
    #displays all of the courses
    courses = student_M.display_Courses()
    courseCodes = courses[2]
    courseName = courses[3]
    if (request.method == "POST"):
        #GENERAL SEARCH
        student_key = request.form['student_key']
        course_key_Code = request.form['course_key_Code']
        student_key_Level = request.form['student_key_Level']
        student_key_Gender = request.form['student_key_Gender']
        
        if len(student_key) < 1:
            flash("You need to input a valid search", category='error')
            return (redirect(url_for('Sbp.students')))
        else:
            search_data = student_M.search_Student(student_key, course_key_Code, student_key_Level, student_key_Gender)
            return render_template('/students/student_results.html', student_key = search_data, Courses = courseCodes, CourseName = courseName)

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
            student_M.edit_Student(idNumberEdit, firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id)
            flash("you have successfully edited the student information!", category='success')
    return redirect(url_for('Sbp.students'))

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
            student_M.add_Students(idNumber, firstName, lastName, courseCode, yearLevel, gender)
            flash("Successfully added the student information!", category='success')
            print("You have successfully added a student")
    return redirect(url_for('Sbp.students'))

#For deleting a selected student
@students_bp.route('/delete_student/<string:students_id>', methods=["GET"])
def delete_student(students_id):
    print('The student has been successfully deleted!')
    flash("you have deleted a student information", category='secondary')
    student_M.delete_Student(students_id)
    return redirect(url_for('Sbp.students'))

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING STUDENTS ENDS IN HERE.#
#<-------------------------------------------------->#
    