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
    #idNumber Checking
    def check_idNumber_Dict(idNumber):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT * from students WHERE idNumber LIKE %s'''
        cursor.execute(SqlQuery, idNumber)
        students = cursor.fetchone()
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
    # Add student with a photo into the database
    def add_Students_p(idNumber, firstName, lastName, courseCode, yearLevel, gender, image):
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''INSERT INTO students(idNumber, firstName, 
            lastName, courseCode, yearLevel, gender, image_id)  VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        SqlValues = (idNumber, firstName, lastName, 
                                courseCode, yearLevel, gender, image)
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
    # Edit a student information with a photo from the database
    def edit_Student_p(idNumberEdit, firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, image, student_id): 
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''UPDATE students SET idNumber=%s, firstName=%s, lastName=%s, 
                        courseCode=%s, yearLevel=%s, gender=%s, image_id=%s WHERE students_id=%s'''
        SqlValues = (idNumberEdit, firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, image, student_id)
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
                SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE  students.idNumber LIKE %s 
                                OR students.firstName LIKE %s
                                OR students.lastName LIKE %s
                                OR students.courseCode LIKE %s
                                OR students.yearLevel LIKE %s
                                OR students.gender LIKE %s'''
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
            print("This is state 1 of the student search results.")
            SqlQuery = '''SELECT students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
                            students.courseCode LIKE %s
                            AND students.firstName LIKE %s
                            OR students.courseCode LIKE %s AND students.lastName LIKE %s
                            OR students.courseCode LIKE %s AND students.idNumber LIKE %s'''
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
            SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
                            students.courseCode LIKE %s AND students.yearLevel LIKE %s AND students.firstName LIKE %s OR 
                            students.courseCode LIKE %s AND students.yearLevel LIKE %s AND students.lastName LIKE %s OR 
                            students.idNumber LIKE %s'''
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
                SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
                                students.yearLevel LIKE %s AND students.firstName LIKE %s OR 
                                students.yearLevel LIKE %s AND students.lastName LIKE %s OR
                                students.yearLevel LIKE %s AND students.idNumber LIKE %s
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
            SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
                            students.gender LIKE %s AND students.firstName LIKE %s OR 
                            students.gender LIKE %s AND students.lastName LIKE %s OR
                            students.gender LIKE %s AND students.idNumber LIKE %s'''
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
            SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
                                students.yearLevel LIKE %s 
                                AND students.gender LIKE %s 
                                AND students.firstName LIKE %s
                            OR  students.yearLevel LIKE %s 
                                AND students.gender LIKE %s 
                                AND students.lastName LIKE %s
                            OR students.idNumber LIKE %s
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
            SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
            students.courseCode LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s AND students.firstName LIKE %s OR 
            students.courseCode LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s AND students.lastName LIKE %s OR
            students.idNumber LIKE %s'''
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
            SqlQuery = '''SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, course_table.courseName, students.yearLevel ,students.gender 
                        FROM students
                        LEFT JOIN course_table ON course_table.courseCode = students.courseCode
                        WHERE
                            students.firstName LIKE %s AND students.courseCode LIKE %s AND students.gender LIKE %s
                            OR students.lastName LIKE %s AND students.courseCode LIKE %s AND students.gender LIKE %s
                            OR students.idNumber LIKE %s'''
            SqlValues = (student_key, course_key_Code, student_key_Gender, 
                                student_key, course_key_Code, student_key_Gender, student_key)
            cursor.execute(SqlQuery, SqlValues)
            search_data = cursor.fetchall()
            db.close()
            cursor.close()
            return search_data 