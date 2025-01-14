'''
    Database SQL models for Students route.
    This models file includes the following funcion:
        – VIEWS
        – ADD STUDENT
        – EDIT STUDENT
        – DELETE STUDENT
        – SEARCH
'''
from src.database import db_connection
import pymysql.cursors


class student_M:

    # Display all students
    def display_Students():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT * FROM students'''
        cursor.execute(SqlQuery)
        students = cursor.fetchall()
        db.close()
        cursor.close()
        return students
    # Display all courses
    def display_Courses():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT * FROM course_table'''
        cursor.execute(SqlQuery)
        courses = cursor.fetchall()
        db.close()
        cursor.close()
        return courses
    # Add student into the database
    def add_Students(idNumber, firstName, lastName, courseCode, yearLevel, gender):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''INSERT INTO students(idNumber, firstName, 
            lastName, courseCode, yearLevel, gender)  VALUES (%s, %s, %s, %s, %s, %s)'''
        SqlValues = (idNumber, firstName, lastName, 
                                courseCode, yearLevel, gender)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Delete a student from the database
    def delete_Student(students_id):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = "DELETE FROM students WHERE students_id = %s"
        SqlValues = (students_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Edit a student information from the datbase
    def edit_Student(idNumberEdit, firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id): 
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''UPDATE students SET idNumber=%s, firstName=%s, lastName=%s, 
                        courseCode=%s, yearLevel=%s, gender=%s WHERE students_id=%s'''
        SqlValues = (idNumberEdit, firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    #  Search a student from the database
    def search_Student(student_key, course_key_Code, student_key_Level, student_key_Gender):
         
        if course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
                db = db_connection()
                cursor = db.cursor()
                print("This is state 1 of the student search results.")
                SqlQuery = '''SELECT * FROM students WHERE idNumber LIKE %s 
                                OR firstName LIKE %s
                                OR lastName LIKE %s
                                OR courseCode LIKE %s
                                OR yearLevel LIKE %s
                                OR gender LIKE %s'''
                SqlValues = (student_key, student_key, student_key, 
                                    student_key, student_key, student_key)
                cursor.execute(SqlQuery, SqlValues)
                search_data = cursor.fetchall()
                db.close()
                cursor.close()
                return search_data      
        
        elif course_key_Code != "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
            print("This is state 2 of the student search results.")
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = '''SELECT * FROM students WHERE
                            courseCode LIKE %s
                            AND firstName LIKE %s
                            OR courseCode LIKE %s AND lastName LIKE %s
                            OR courseCode LIKE %s AND idNumber LIKE %s'''
            SqlValues = (course_key_Code, student_key, course_key_Code, 
                                    student_key, course_key_Code, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data   
        
        elif course_key_Code != "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender == "By Gender":
            print("This is state 3 of the student search results.")
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = '''SELECT * FROM students WHERE
                            courseCode LIKE %s AND yearLevel LIKE %s AND firstName LIKE %s OR 
                            courseCode LIKE %s AND yearLevel LIKE %s AND lastName LIKE %s OR 
                            idNumber LIKE %s'''
            SqlValues = (course_key_Code, student_key_Level, student_key, 
                                 course_key_Code, student_key_Level, student_key, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data 
        
        elif course_key_Code == "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender == "By Gender":
                print("This is state 4 of the student search results.")
                db = db_connection()
                cursor = db.cursor()
                SqlQuery = '''SELECT * FROM students WHERE
                                yearLevel LIKE %s AND firstName LIKE %s OR 
                                yearLevel LIKE %s AND lastName LIKE %s OR
                                yearLevel LIKE %s AND idNumber LIKE %s
                                '''
                SqlValues = (student_key_Level, student_key, student_key_Level, 
                                    student_key, student_key_Level, student_key)
                cursor.execute(SqlQuery, SqlValues)
                search_data = cursor.fetchall()
                db.close()
                cursor.close()
                return search_data 
            
        elif course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 5 of the student search results.")
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = '''SELECT * FROM students WHERE
                            gender LIKE %s AND firstName LIKE %s OR 
                            gender LIKE %s AND lastName LIKE %s OR
                            gender LIKE %s AND idNumber LIKE %s'''
            SqlValues = (student_key_Gender, student_key, student_key_Gender, 
                                student_key, student_key_Gender, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data 
        
        elif course_key_Code == "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 6 of the student search results.")
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = '''SELECT * FROM students WHERE 
                                yearLevel LIKE %s 
                                AND gender LIKE %s 
                                AND firstName LIKE %s
                            OR  yearLevel LIKE %s 
                                AND gender LIKE %s 
                                AND lastName LIKE %s
                            OR idNumber LIKE %s
                                '''
            SqlValues = (student_key_Level, student_key_Gender, student_key, 
                                student_key_Level, student_key_Gender, student_key, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data 
        
        elif course_key_Code != "By Course Code" and student_key_Level != "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 7 of the student search results.")     
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = '''SELECT * FROM students WHERE 
            courseCode LIKE %s AND yearLevel LIKE %s AND gender LIKE %s AND firstName LIKE %s OR 
            courseCode LIKE %s AND yearLevel LIKE %s AND gender LIKE %s AND lastName LIKE %s OR
            idNumber = %s'''
            SqlValues = (course_key_Code, student_key_Level, student_key_Gender, student_key, 
                            course_key_Code, student_key_Level, student_key_Gender, student_key, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data 
        
        elif course_key_Code != "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender != "By Gender":
            print("This is state 8 of the student search results.")
            db = db_connection()
            cursor = db.cursor()
            SqlQuery = '''SELECT * FROM students WHERE
                            firstName LIKE %s AND courseCode LIKE %s AND gender LIKE %s
                            OR lastName LIKE %s AND courseCode LIKE %s AND gender LIKE %s
                            OR idNumber'''
            SqlValues = (student_key, course_key_Code, student_key_Gender, 
                                student_key, course_key_Code, student_key_Gender, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data 