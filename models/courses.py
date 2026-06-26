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
        cursor = db.cursor(pymysql.cursors.DictCursor)
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
    # take all college names
    def check_collegeCode(collegeCode):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT college_table.collegeName FROM college_table WHERE collegeCode = %s'''
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


    def search_filter(course_key_Code, course_key_Name, college_key_Code):

        if course_key_Code:
            sqlQuery = '''SELECT * FROM course_table WHERE courseCode LIKE %s'''
            sqlValues = (course_key_Code)

        if course_key_Name:
            sqlQuery = '''SELECT * FROM course_table WHERE courseName LIKE %s'''
            sqlValues = (course_key_Name)

        if college_key_Code:
            sqlQuery = '''SELECT * FROM course_table WHERE collegeCode LIKE %s'''
            sqlValues = (college_key_Code)

        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sqlQuery, sqlValues)
        search_data = cursor.fetchall()
        cursor.close()
        db.close()
        return search_data

    # searching for a course from the database
    def search_Course(course_key, course_key_Name, course_key_Code, college_key_Code):

        if course_key:
            sqlQuery = '''SELECT * FROM course_table WHERE courseCode LIKE %s OR courseName LIKE %s OR collegeCode LIKE %s'''
            sqlValues = (course_key, course_key, course_key)

        if course_key_Code:
            sqlQuery = '''SELECT * FROM course_table WHERE courseCode LIKE %s OR courseCode LIKE %s'''
            sqlValues = (course_key, course_key_Code)

        if course_key_Name:
            sqlQuery = '''SELECT * FROM course_table WHERE courseCode LIKE %s OR courseName LIKE %s'''
            sqlValues = (course_key, course_key_Name)

        if college_key_Code:
            sqlQuery = '''SELECT * FROM course_table WHERE courseCode LIKE %s OR collegeCode LIKE %s'''
            sqlValues = (course_key, college_key_Code)

        if course_key_Code and course_key_Name:
            sqlQuery = '''SELECT * FROM course_table WHERE courseName LIKE %s OR courseCode LIKE %s OR collegeCode LIKE %s
             OR courseCode LIKE %s OR courseName LIKE %s'''
            sqlValues = (course_key, course_key, course_key, course_key_Code, course_key_Name)

        if course_key_Code and college_key_Code:
            sqlQuery = '''SELECT * FROM course_table WHERE courseName LIKE %s OR courseCode LIKE %s OR collegeCode LIKE %s
             OR courseCode LIKE %s OR collegeCode LIKE %s'''
            sqlValues = (course_key, course_key, course_key, course_key_Code, college_key_Code)

        if course_key_Name and college_key_Code:
            sqlQuery = '''SELECT * FROM course_table WHERE courseName LIKE %s OR courseCode LIKE %s OR collegeCode LIKE %s
             OR courseName LIKE %s OR collegeCode LIKE %s'''
            sqlValues = (course_key, course_key, course_key, course_key_Code, college_key_Code)

        if course_key_Code and college_key_Code and course_key_Name:
            sqlQuery = '''SELECT * FROM course_table WHERE
                    courseCode LIKE %s OR courseName LIKE %s AND collegeCode LIKE %s OR
                    courseName LIKE %s OR courseCode LIKE %s AND collegeCode LIKE %s OR
                    collegeCode LIKE %s OR courseCode LIKE %s AND courseName LIKE %s'''
            sqlValues = (course_key, course_key_Name, college_key_Code,
                        course_key, course_key_Code, college_key_Code,
                        course_key, course_key_Code, course_key_Name)

        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sqlQuery, sqlValues)
        search_data = cursor.fetchall()
        cursor.close()
        db.close()
        return search_data
