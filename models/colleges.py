'''
    Database SQL models for Colleges route.
    This models file includes the following funcion:
        – VIEWS
        – ADD Colleges
        – EDIT Colleges
        – DELETE Colleges
        – SEARCH Colleges
'''
from src.database import db_connection
import pymysql.cursors

class college_M:
    # Display colleges
    def display_Colleges():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT * FROM college_table'''
        cursor.execute(SqlQuery)
        colleges = cursor.fetchall()
        cursor.close()
        db.close()
        return colleges    
    # Edit college information from the database
    def edit_College(collegeCodeEdit, collegeNameEdit, college_id):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = "UPDATE college_table SET collegeCode=%s, collegeName=%s WHERE college_id=%s"
        SqlValues = (collegeCodeEdit, collegeNameEdit, college_id)
        cursor.execute( SqlQuery, SqlValues)
        db.commit()
        cursor.close()
        db.close()
        return college_M.display_Colleges()
    # Add college information into the database
    def add_College(collegeCode, collegeName):
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = "INSERT INTO college_table(collegeCode, collegeName) VALUES (%s, %s)"
            SqlValues = (collegeCode, collegeName)
            cursor.execute(SqlQuery, SqlValues)
            db.commit()
            cursor.close()
            db.close()
            return college_M.display_Colleges()
    
    # check college code for edit
    def check_CollegeCode(collegeCode):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT college_table.collegeCode FROM college_table WHERE collegeCode = %s'''
        cursor.execute(SqlQuery, collegeCode,)
        collegeCode_unique = cursor.fetchone()
        db.close()
        cursor.close()
        return collegeCode_unique
    
    # check college name for edit
    def check_CollegeName(collegeName):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT college_table.collegeName FROM college_table WHERE collegeName = %s'''
        cursor.execute(SqlQuery, collegeName,)
        collegeName_unique = cursor.fetchone()
        db.close()
        cursor.close()
        return collegeName_unique
            
    # Delete college information
    def delete_College(collegeCode):
        
        db = db_connection()
        cursor = db.cursor()
        # deleting college data
        SqlQuery = "DELETE FROM college_table WHERE collegeCode = %s"
        SqlValues = (collegeCode)
        cursor.execute( SqlQuery, SqlValues)
        db.commit()
        
        # setting college data into N/A on courses table
        SqlQuery = "UPDATE course_table SET collegeCode = 'N/A' WHERE collegeCode = %s"
        SqlValues = (collegeCode)
        cursor.execute( SqlQuery, SqlValues)
        
        db.commit()
        cursor.close()
        db.close()
        return college_M.display_Colleges()
    # search college information from the database
    def search_College(college_key, college_key_Code, college_key_Name):
         
         if college_key_Code == "By College Code" and college_key_Name == "By College Name":
            print("This is route 1")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM college_table WHERE collegeCode LIKE %s OR collegeName LIKE %s''', 
                        (college_key, college_key))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        #THIS IS FOR SEARCHING COLLEGE CODE WITH EXCLUSIVITY
         elif college_key_Code != "By College Code" and college_key_Name == "By College Name":
            print("This is route 2")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM college_table WHERE collegeCode LIKE %s AND collegeName LIKE %s''', 
                        (college_key_Code, college_key))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        #THIS IS FOR SEARCHING COLLEGE NAME FIELDS WITH EXCLUSIVITY
         elif college_key_Code == "By College Code" and college_key_Name != "By College Name":
            print("This is route 3")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM college_table WHERE collegeName LIKE %s AND collegeCode LIKE %s''', 
                        (college_key_Name, college_key))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        #THIS IS FOR SEARCH COLLEGE CODE AND COLLEGE NAME FIELDS WITH EXCLUSIVITY
         elif college_key_Code != "By College Code" and college_key_Name != "By College Name":
            print("This is route 4")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM college_table WHERE collegeName LIKE %s AND collegeCode LIKE %s''', 
                        (college_key_Name, college_key_Code))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data