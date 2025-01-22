from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
import pymysql.cursors
from config import SECRET_KEY
from src.database import db_connection
from models.colleges import college_M
#from models.courses import course_M
#from models.students import student_M



colleges_bp = Blueprint("Clbp", __name__,  template_folder='/templates')



#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COLLEGES STARTS IN HERE.#
#<-------------------------------------------------->#

#This is for accessing college table and its actions:
@colleges_bp.route('/colleges')
def colleges():
    college = college_M.display_Colleges()
    return render_template('/colleges/colleges.html', College=college)

#For editing a college information
@colleges_bp.route('/edit_college', methods=["POST"])
def edit_college():
    if request.method == "POST":
        print('successfully edited the select item')
        college_id = request.form['college_id']
        collegeCodeEdit = request.form['collegeCodeEdit']
        collegeNameEdit = request.form['collegeNameEdit']
        
        collegeCode_Checking = college_M.check_CollegeCode(collegeCodeEdit)
        collegeName_Checking = college_M.check_CollegeName(collegeNameEdit)
        
        if len(collegeCodeEdit) < 1:
            flash("You have to input a valid college!", category="error")

        elif len(collegeNameEdit) < 1:
            flash("You have to input a valid college!", category="error")
        
        elif collegeCode_Checking and collegeName_Checking:
            flash("College already exists!", category="error")
            
        else:
            college_M.edit_College(collegeCodeEdit, collegeNameEdit, college_id)
            flash("You have successfuly edited a college!", category="success")
            
    return redirect(url_for('Clbp.colleges'))

#For searching an input for college_table
@colleges_bp.route('/college_search', methods=["POST"])
def college_search():
    if (request.method == "POST"):
        #GENERAL SEARCH
        college_key = request.form['college_key']
        college_key_Code = request.form['college_key_Code']
        college_key_Name = request.form['college_key_Name']
        
        if len(college_key) < 1:
            flash("You need to input a valid search", category='error')
            return (redirect(url_for('Clbp.colleges')))
          #  return render_template('college_results.html', college_key = search_data)
        if len(college_key) > 1:
            search_data = college_M.search_College(college_key, college_key_Code, college_key_Name)
            return render_template('/colleges/college_results.html', College = search_data)
        else:
            return render_template('/colleges/colleges.html')
    
#For deleting a selected college item
@colleges_bp.route('/delete_college/<string:collegeCode>', methods=["GET"])
def delete_college(collegeCode):
    print('The college has been successfully deleted!')
    college_M.delete_College(collegeCode)
    flash("You have deleted college information. It will take effect on the courses under the deleted. ", category='secondary')
    return redirect(url_for('Clbp.colleges'))

#For adding a new college information
@colleges_bp.route('/add_college', methods=["GET", "POST"])
def add_college():
    if request.method == "POST":
        collegeCode = request.form['collegeCode']
        collegeName = request.form['collegeName']
        
        collegeCode_unique = college_M.check_CollegeCode(collegeCode)
        collegeName_unique = college_M.check_CollegeName(collegeName)
        
        if len(collegeCode) < 1:
            flash("You have to input a valid college!", category="error")
        elif collegeCode_unique:
            flash("College already exists!", category="error")
        elif collegeName_unique:
            flash("College already exists!", category="error")
        elif len(collegeName) < 1:
            flash("You have to input a valid college!", category="error")
        else:
            college_M.add_College(collegeCode, collegeName)
            flash("You have successfuly added college!", category="success")
    return redirect(url_for('Clbp.colleges'))

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COLLEGES ENDS IN HERE.#
#<-------------------------------------------------->#
