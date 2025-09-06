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
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = ''' SELECT students.students_id, students.idNumber, students.firstName,  
        students.lastName, students.courseCode, students.course_id,
        students.yearLevel, students.gender, students.image_id FROM students'''
        
        
              #  '''SELECT students.students_id, students.idNumber, students.firstName, students.lastName, students.courseCode,
              #      students.course_id, students.yearLevel, students.gender, students.image_id, college_table.collegeName FROM students 
              #      JOIN course_table ON students.courseCode = course_table.courseCode
              #      JOIN college_table ON course_table.collegeCode = college_table.collegeCode'''
        cursor.execute(SqlQuery)
        students = cursor.fetchall()
        db.close()
        cursor.close()
        return students

    #idNumber Checking
    def check_idNumber_Dict(idNumber):
        db = db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        SqlQuery = '''SELECT students.idNumber FROM students WHERE idNumber = %s'''
        cursor.execute(SqlQuery, idNumber)
        idNumber_unique = cursor.fetchone()
        db.close()
        cursor.close()
        return idNumber_unique

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

    # Display courses alongside colleges
    def display_course_college():
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''SELECT course_table.courseCode, college_table.collegeName 
        FROM course_table RIGHT JOIN college_table ON college_table.collegeCode = course_table.collegeCode'''
        cursor.execute(SqlQuery)
        courses_colleges = cursor.fetchall()
        db.close()
        cursor.close()
        return courses_colleges

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
    def edit_Student(firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id): 
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''UPDATE students SET firstName=%s, lastName=%s, 
                        courseCode=%s, yearLevel=%s, gender=%s WHERE students_id=%s'''
        SqlValues = (firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, student_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()
    # Edit a student information with a photo from the database
    def edit_Student_p(firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, image, student_id): 
        db = db_connection()
        cursor = db.cursor()
        SqlQuery = '''UPDATE students SET firstName=%s, lastName=%s, 
                        courseCode=%s, yearLevel=%s, gender=%s, image_id=%s WHERE students_id=%s'''
        SqlValues = (firstNameEdit, lastNameEdit, 
                            courseCodeEdit, yearLevelEdit, genderEdit, image, student_id)
        cursor.execute(SqlQuery, SqlValues)
        db.commit()
        db.close()
        cursor.close()
        return student_M.display_Students()

    #  Search a student from the database
    def search_student_2(student_key_1, student_key_2, course_key_Code, student_key_Level, student_key_Gender):
        
        if course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
                db = db_connection()
                cursor = db.cursor()
                print("This is the double string of the student search results.")
                SqlQuery = '''
                        SELECT students.students_id ,students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, students.yearLevel, students.gender FROM students WHERE students.idNumber LIKE %s 
                        OR students.firstName LIKE %s OR students.lastName LIKE %s'''
                SqlValues = (student_key_1, student_key_1, student_key_2)
                cursor.execute(SqlQuery, SqlValues)
                search_data = cursor.fetchall()
                db.close()
                cursor.close()
                return search_data



    def search_Student(student_key_1, course_key_Code, student_key_Level, student_key_Gender):
   
        if course_key_Code == "By Course Code" and student_key_Level == "By Year Level" and student_key_Gender == "By Gender":
                db = db_connection()
                cursor = db.cursor()
                print("This is state 1 of the student search results.")
                SqlQuery = '''
                        SELECT students.students_id, students.image_id, students.idNumber, students.firstName, students.lastName, 
                        students.courseCode, college_table.collegeName, students.yearLevel ,students.gender FROM students 
                        JOIN course_table ON students.courseCode = course_table.courseCode
                        JOIN college_table ON course_table.collegeCode = college_table.collegeCode 
                        WHERE  students.idNumber LIKE %s 
                                OR students.firstName LIKE %s
                                OR students.lastName LIKE %s
                                OR students.courseCode LIKE %s
                                OR students.yearLevel LIKE %s
                                OR students.gender LIKE %s'''
                SqlValues = (student_key_1, student_key_1, student_key_1, 
                                    student_key_1, student_key_1, student_key_1)
                cursor.execute(SqlQuery, SqlValues)
                search_data = cursor.fetchall()
                db.close()
                cursor.close()
                return search_data

        