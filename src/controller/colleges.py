from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
import pymysql.cursors
from config import SECRET_KEY
from src.database import db_connection
from models.colleges import college_M

import re
#from models.courses import course_M
#from models.students import student_M

colleges_bp = Blueprint("Clbp", __name__,  template_folder='/templates')

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COLLEGES STARTS IN HERE.#
#<-------------------------------------------------->#

#This is for accessing college table and its actions:
@colleges_bp.route('/colleges', methods=['GET', 'POST'])
def colleges():

    if request.method == "GET":
        college = college_M.display_Colleges()
        return render_template('/colleges/colleges.html', College=college)
    
    # Searching a college
    if request.method == "POST":
        college = college_M.display_Colleges()
        try:
            college_key = request.form['college_key']
            college_key_Code = request.form['college_key_Code']
            college_key_Name = request.form['college_key_Name']

            if college_key_Code == "By College Code":
                college_key_Code = None
                print(f"college_key_Name has no input")

            if college_key_Name == "By College Name":
                college_key_Name = None
                print(f"college_key_Name has no input")
            
            if len(college_key) < 1:
                flash("You need to input a valid search", category='error')
                return (redirect(url_for('Clbp.colleges')))
              
            if len(college_key) > 1:
                # Refactor this into fetching one query.
                search_data = college_M.search_College(college_key, college_key_Code, college_key_Name)
                return render_template('/colleges/college_results.html', College = search_data, search_filters = college)
            else:
                return render_template('/colleges/colleges.html')
        except Exception as e:
            flash(f"Invalid search. {e} occured!", category='error')


#For editing a college information
@colleges_bp.route('/edit_college', methods=["POST"])
def edit_college():
    if request.method == "POST":
        print('successfully edited the select item')
        college_id = request.form['college_id']
        collegeCodeEdit = request.form['collegeCodeEdit']
        collegeNameEdit = request.form['collegeNameEdit']
        
        try:
            collegeCode_Checking = college_M.check_CollegeCode(collegeCodeEdit)
            collegeName_Checking = college_M.check_CollegeName(collegeNameEdit)
            
            if len(collegeCodeEdit) < 1:
                flash("You have to input a valid college!", category="error")

            elif len(collegeNameEdit) < 1:
                flash("You have to input a valid college!", category="error")
            
            elif collegeCode_Checking and collegeName_Checking:
                flash("College already exists!", category="error")
                
            else:
                captCollegeCode = collegeCodeEdit.upper()
                captCollegeName = collegeNameEdit.title().replace("Of", "of")

                college_M.edit_College(captCollegeCode, captCollegeName, college_id)

                flash("You have successfuly edited a college!", category="success")

        except Exception as e:
            flash(f"Invalid editing item. {e} occured!", category="error")

    return redirect(url_for('Clbp.colleges'))

   
#For deleting a selected college item
@colleges_bp.route('/delete_college/<string:collegeCode>', methods=["GET"])
def delete_college(collegeCode):
    try:
        college_M.delete_College(collegeCode)
        print('The college has been successfully deleted!')
        flash(f"You have deleted college information. It will take effect on the courses under the deleted {collegeCode}.", category='secondary')
        return redirect(url_for('Clbp.colleges'))
    except Exception as e:
        flash(f"Invalid deletion {e}", category='secondary')
        return redirect(url_for('Clbp.colleges'))

#For adding a new college information
@colleges_bp.route('/add_college', methods=["GET", "POST"])
def add_college():
    if request.method == "POST":
        collegeCode = request.form['collegeCode']
        collegeName = request.form['collegeName']
  
        try:
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
                captCollegeCode = collegeCode.upper()
                captCollegeName = collegeName.title().replace("Of", "of")

                college_M.add_College(captCollegeCode, captCollegeName)
                flash("You have successfuly added college!", category="success")
                
        except Exception as e:
            flash(f"Invalid adding item to the database. {e} occured!", category="error")

    return redirect(url_for('Clbp.colleges'))
            
#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COLLEGES ENDS IN HERE.#
#<-------------------------------------------------->#
