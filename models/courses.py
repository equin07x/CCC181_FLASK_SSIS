'''
    Database SQL models for Courses route.
    This models file includes the following funcion:
        – VIEWS
        – ADD Courses
        – EDIT Courses
        – DELETE Courses
        – SEARCH Courses
'''
from src.database import db_connection
import pymysql.cursors

class course_M:
    # Display the courses from the database
    def display_Courses():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT * FROM course_table'''
        cursor.execute(SqlQuery)
        courses = cursor.fetchall()
        cursor.close()
        db.close()
        return courses
    # Display the colleges from the database
    def display_Colleges():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT * FROM college_table'''
        cursor.execute(SqlQuery)
        college = cursor.fetchall()
        cursor.close()
        db.close()
        return college
    # Courses Checking
      # check course code for edit
    def check_courseCode(courseCode):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT course_table.courseCode FROM course_table WHERE courseCode = %s'''
        cursor.execute(SqlQuery, courseCode,)
        course_Unique = cursor.fetchone()
        db.close()
        cursor.close()
        return course_Unique
    # check course name for edit
    def check_courseName(courseName):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT course_table.courseName FROM course_table WHERE courseCode = %s'''
        cursor.execute(SqlQuery, courseName,)
        course_Unique = cursor.fetchone()
        db.close()
        cursor.close()
        return course_Unique
    # check college for edit
    def check_collegeCode(collegeCode):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT course_table.collegeCode FROM course_table WHERE collegeCode = %s'''
        cursor.execute(SqlQuery, collegeCode,)
        course_Unique = cursor.fetchone()
        db.close()
        cursor.close()
        return course_Unique
    # Edit a course information from the database
    def edit_Course(courseCodeEdit, courseNameEdit, collegeCodeEdit, course_id):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = "UPDATE course_table SET courseCode=%s, courseName=%s, collegeCode=%s WHERE course_id=%s"
        SqlValues = (courseCodeEdit, courseNameEdit, collegeCodeEdit, course_id)
        cursor.execute(SqlQuery, SqlValues)
        cursor.close()
        db.commit()
        db.close()
        return course_M.display_Courses()
    # Add a course information into the datbase
    def add_Course(courseCode, courseName, collegeCode):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = "INSERT INTO course_table( courseCode, courseName, collegeCode) VALUES (%s, %s, %s)"
        SqlValues = (courseCode, courseName, collegeCode)
        cursor.execute(SqlQuery, SqlValues)
        cursor.close()
        db.commit()
        db.close()
        return course_M.display_Courses()
    # Delete a course information from the datbase
    def delete_Course(courseCode):
        db = db_connection()
        cursor = db.cursor()
        #Deleting the course
        SqlQuery = "DELETE FROM course_table WHERE courseCode = %s"
        SqlValues = (courseCode)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        #Setting the course into N/A on the student's database
        SqlQuery = "UPDATE students SET courseCode = 'N/A' WHERE courseCode = %s"
        SqlValues = (courseCode)
        cursor.execute(SqlQuery, SqlValues)
        cursor.close()
        db.commit()
        db.close()
        return course_M.display_Courses()
    # searching for a course from the database
    def search_Course(course_key, course_key_Name, course_key_Code, college_key_Code):
        
        if course_key_Code == "By Course Code" and course_key_Name == "By Course Name" and college_key_Code == "By College Code":
            print("This is state 1 for searching courses")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s OR courseName LIKE %s OR collegeCode LIKE %s''', 
                        (course_key, course_key, course_key))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        #THIS IS FOR SEARCHING COURSES CODE WITH EXCLUSIVITY
        elif course_key_Code != "By Course Code" and course_key_Name == "By Course Name" and college_key_Code == "By College Code":
            print("This is state 2 for searching courses")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM course_table WHERE courseName LIKE %s OR collegeCode LIKE %s AND courseCode LIKE %s ''', 
                        (course_key, course_key, course_key_Code))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        #THIS IS FOR SEARCHING COURSES NAME WITH EXCLUSIVITY
        elif course_key_Code == "By Course Code" and course_key_Name != "By Course Name" and college_key_Code == "By College Code":
            print("This is state 3 for searching courses")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  OR collegeCode LIKE %s AND courseName LIKE %s ''', 
                        (course_key, course_key, course_key_Name))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        
        #THIS IS FOR SEARCHING COLLEGE CODE FIELDS WITH EXCLUSIVITY
        elif course_key_Code == "By Course Code" and course_key_Name == "By Course Name" and college_key_Code != "By College Code":
            print("This is state 4 for searching courses")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  OR courseName LIKE %s AND collegeCode LIKE %s''', 
                        (course_key, course_key, college_key_Code))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data
        
        #THIS IS FOR SEARCHING FIELDS WITH EXCLUSIVITY
        elif course_key_Code != "By Course Code" and course_key_Name != "By Course Name" and college_key_Code != "By College Code":
            print("This is state 5 for searching courses")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s  AND courseName LIKE %s AND collegeCode LIKE %s''', 
                        (course_key_Code, course_key_Name, college_key_Code))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data

        elif course_key_Code == "By Course Code" and course_key_Name != "By Course Name" and college_key_Code != "By College Code":
            print("This is state 6 for searching courses")
            db = db_connection()
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM course_table WHERE courseCode LIKE %s OR courseName LIKE %s AND collegeCode LIKE %s''', 
                        (course_key_Code, course_key_Name, college_key_Code))
            search_data = cursor.fetchall()
            cursor.close()
            db.close()
            return search_data