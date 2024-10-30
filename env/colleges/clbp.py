from flask import render_template, request, url_for, flash, redirect
from flask import Blueprint
from env import db


colleges_bp = Blueprint('clbp', __name__, template_folder="templates")

cursor = db.cursor()
def commit():
    db.commit()
    

#<-------------------------------------------------->#
#THE CODES RELATED FOR HANDLING COLLEGES STARTS IN HERE.#
#<-------------------------------------------------->#

#This is for accessing college table and its actions:

#For editing a college information
@colleges_bp.route('/edit_college', methods=["GET","POST"])
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
    return redirect(url_for('clbp.colleges'))

#For searching an input for college_table
@colleges_bp.route('/college_search', methods=["POST"])
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
            return render_template('/colleges/college_results.html', college_key = search_data)
        
        #THIS IS FOR SEARCHING COLLEGE CODE WITH EXCLUSIVITY
        elif request.form['college_key_Code'] != "By College Code" and request.form['college_key_Name'] == "By College Name":
            print("This is route 2")
            college_key = request.form['college_key']
            college_key_Code = request.form['college_key_Code']
            cursor.execute('''SELECT * FROM college_table WHERE collegeCode LIKE %s AND collegeName LIKE %s''', 
                        (college_key_Code, college_key))
            search_data = cursor.fetchall()
            return render_template('/colleges/college_results.html', college_key = search_data)
        
        #THIS IS FOR SEARCHING COLLEGE NAME FIELDS WITH EXCLUSIVITY
        elif request.form['college_key_Code'] == "By College Code" and request.form['college_key_Name'] != "By College Name":
            print("This is route 3")
            college_key = request.form['college_key']
            college_key_Name = request.form['college_key_Name']
            cursor.execute('''SELECT * FROM college_table WHERE collegeName LIKE %s AND collegeCode LIKE %s''', 
                        (college_key_Name, college_key))
            search_data = cursor.fetchall()
            return render_template('/colleges/college_results.html', college_key = search_data)
        
        #THIS IS FOR SEARCH COLLEGE CODE AND COLLEGE NAME FIELDS WITH EXCLUSIVITY
        elif request.form['college_key_Code'] != "By College Code" and request.form['college_key_Name'] != "By College Name":
            print("This is route 4")
            college_key = request.form['college_key']
            college_key_Name = request.form['college_key_Name']
            college_key_Code = request.form['college_key_Code']
            cursor.execute('''SELECT * FROM college_table WHERE collegeName LIKE %s AND collegeCode LIKE %s''', 
                        (college_key_Name, college_key_Code))
            search_data = cursor.fetchall()
            return render_template('/colleges/college_results.html', college_key = search_data)
        else:
            return render_template('/colleges/college_results.html')
    
#For deleting a selected college item
@colleges_bp.route('/delete_college/<string:collegeCode>', methods=["GET"])
def delete_college(collegeCode):
    print('The college has been successfully deleted!')
    cursor.execute("DELETE FROM college_table WHERE collegeCode = %s", (collegeCode))
    cursor.execute("UPDATE course_table SET collegeCode = 'N/A' WHERE collegeCode = %s", (collegeCode))
    flash("You have deleted college information. It will take effect on the courses under the deleted. ", category='secondary')
    commit()
    return redirect(url_for('colleges'))

#For adding a new college information
@colleges_bp.route('/add_college', methods=["GET", "POST"])
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

