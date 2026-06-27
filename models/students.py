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
        SqlQuery = '''
                    SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    '''
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

    def filter_search(course_key_Code, student_key_Gender, student_key_Level):

        if course_key_Code:
            print(f"Search Filter: {course_key_Code}\n")
            SqlQuery = '''
                SELECT
                students.students_id,
                students.idNumber,
                students.firstName,
                students.lastName,
                students.courseCode,
                students.course_id,
                students.yearLevel,
                students.gender,
                students.image_id,
                COALESCE(college_table.collegeName, 'N/A') AS collegeName
            FROM students
            LEFT JOIN course_table
                ON students.courseCode = course_table.courseCode
            LEFT JOIN college_table
                ON course_table.collegeCode = college_table.collegeCode
            WHERE
                (students.courseCode LIKE %s)'''
            SqlValues = (course_key_Code)

        elif student_key_Gender:
            print(f"Search Filter: {student_key_Gender}\n")
            SqlQuery = '''
                    SELECT
                    students.students_id,
                    students.idNumber,
                    students.firstName,
                    students.lastName,
                    students.courseCode,
                    students.course_id,
                    students.yearLevel,
                    students.gender,
                    students.image_id,
                    COALESCE(college_table.collegeName, 'N/A') AS collegeName
                FROM students
                LEFT JOIN course_table
                    ON students.courseCode = course_table.courseCode
                LEFT JOIN college_table
                    ON course_table.collegeCode = college_table.collegeCode
                WHERE
                    (students.gender LIKE %s)'''
            SqlValues = (student_key_Gender)

        elif student_key_Level:
            print(f"Search Filter: {student_key_Level}\n")
            SqlQuery = '''
                SELECT
                    students.students_id,
                    students.idNumber,
                    students.firstName,
                    students.lastName,
                    students.courseCode,
                    students.course_id,
                    students.yearLevel,
                    students.gender,
                    students.image_id,
                    COALESCE(college_table.collegeName, 'N/A') AS collegeName
                FROM students
                LEFT JOIN course_table
                    ON students.courseCode = course_table.courseCode
                LEFT JOIN college_table
                    ON course_table.collegeCode = college_table.collegeCode
                WHERE
                    (students.yearLevel LIKE %s)'''
            SqlValues = (student_key_Level)

        db = db_connection()
        cursor = db.cursor()
        cursor.execute(SqlQuery, SqlValues)
        search_data = cursor.fetchall()
        db.close()
        cursor.close()
        return search_data

    def search_combine(course_key_Code, student_key_Level, student_key_Gender):

        if course_key_Code and student_key_Level:
            print(f"Search Filter: {course_key_Code} and {student_key_Level}\n")
            SqlQuery = '''
                 SELECT
                         students.students_id,
                         students.idNumber,
                         students.firstName,
                         students.lastName,
                         students.courseCode,
                         students.course_id,
                         students.yearLevel,
                         students.gender,
                         students.image_id,
                         COALESCE(college_table.collegeName, 'N/A') AS collegeName
                     FROM students
                     LEFT JOIN course_table
                         ON students.courseCode = course_table.courseCode
                     LEFT JOIN college_table
                         ON course_table.collegeCode = college_table.collegeCode
                     WHERE
                         (students.courseCode LIKE %s AND students.yearLevel LIKE %s)'''
            SqlValues = (course_key_Code, student_key_Level)

        if course_key_Code and student_key_Gender:
            print(f"Search Filter: {course_key_Code} and {student_key_Gender}\n")
            SqlQuery = '''
                SELECT
                    students.students_id,
                    students.idNumber,
                    students.firstName,
                    students.lastName,
                    students.courseCode,
                    students.course_id,
                    students.yearLevel,
                    students.gender,
                    students.image_id,
                    COALESCE(college_table.collegeName, 'N/A') AS collegeName
                FROM students
                LEFT JOIN course_table
                    ON students.courseCode = course_table.courseCode
                LEFT JOIN college_table
                    ON course_table.collegeCode = college_table.collegeCode
                WHERE
                    (students.courseCode LIKE %s AND students.gender LIKE %s)'''
            SqlValues = (course_key_Code, student_key_Gender)

        elif student_key_Gender and student_key_Level:
            print(f"Search Filter: {student_key_Gender} and {student_key_Level}\n")
            SqlQuery = '''
                SELECT
                    students.students_id,
                    students.idNumber,
                    students.firstName,
                    students.lastName,
                    students.courseCode,
                    students.course_id,
                    students.yearLevel,
                    students.gender,
                    students.image_id,
                    COALESCE(college_table.collegeName, 'N/A') AS collegeName
                FROM students
                LEFT JOIN course_table
                    ON students.courseCode = course_table.courseCode
                LEFT JOIN college_table
                    ON course_table.collegeCode = college_table.collegeCode
                WHERE
                    (students.gender LIKE %s AND students.yearLevel LIKE %s)'''
            SqlValues = (student_key_Gender, student_key_Level)

        if course_key_Code and student_key_Gender and student_key_Level:
            print(f"Search Filter: { course_key_Code } and  { student_key_Gender } and { student_key_Level }\n")
            SqlQuery = '''
                SELECT
                    students.students_id,
                    students.idNumber,
                    students.firstName,
                    students.lastName,
                    students.courseCode,
                    students.course_id,
                    students.yearLevel,
                    students.gender,
                    students.image_id,
                    COALESCE(college_table.collegeName, 'N/A') AS collegeName
                FROM students
                LEFT JOIN course_table
                    ON students.courseCode = course_table.courseCode
                LEFT JOIN college_table
                    ON course_table.collegeCode = college_table.collegeCode
                WHERE
                    (students.courseCode LIKE %s AND students.gender LIKE %s AND students.yearLevel LIKE %s)'''
            SqlValues = (course_key_Code, student_key_Gender, student_key_Level)

        db = db_connection()
        cursor = db.cursor()
        cursor.execute(SqlQuery, SqlValues)
        search_data = cursor.fetchall()
        db.close()
        cursor.close()
        return search_data

    def search_Student(student_key, course_key_Code, student_key_Level, student_key_Gender):

        student_keys = student_key.title().strip().split()

        if len(student_keys) == 1:
            print(f"Search Item: {student_keys[0]}")
            SqlQuery = '''
                    SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s
                         OR students.lastName LIKE %s
                         OR students.idNumber LIKE %s
                         OR students.courseCode LIKE %s
                         OR students.gender LIKE %s
                         OR students.yearLevel LIKE %s);

                    '''
            SqlValues = (student_keys[0], student_keys[0], student_keys[0], student_keys[0], student_keys[0],  student_keys[0])

        if len(student_keys) == 2:
            print(f"Search Item: {student_keys[0]} {student_keys[1]}")
            SqlQuery = '''
                    SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                    (firstName LIKE %s OR lastName LIKE %s OR idNumber LIKE %s)'''
            SqlValues = (student_keys[0], student_keys[1], student_keys[0])

        # Course Code constraint
        if course_key_Code and len(student_keys) == 1:
                print(f"Search Filter: {course_key_Code}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.courseCode LIKE %s) OR
                        (students.lastName LIKE %s AND students.courseCode LIKE %s) OR
                        (students.idNumber LIKE %s AND students.courseCode LIKE %s)'''
                SqlValues = (student_keys[0], course_key_Code, student_keys[0], course_key_Code, student_keys[0], course_key_Code)

        if course_key_Code and len(student_keys) == 2:
                print(f"Search Filter: {course_key_Code}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.courseCode LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], course_key_Code)

        # Year Level constraint
        if student_key_Level and len(student_keys) == 1:
                print(f"Search Filter: {student_key_Level}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.yearLevel LIKE %s) OR
                        (students.lastName LIKE %s AND students.yearLevel LIKE %s) OR
                        (students.idNumber LIKE %s AND students.yearLevel LIKE %s)'''

                SqlValues = (student_keys[0], student_key_Level, student_keys[0], student_key_Level, student_keys[0], student_key_Level)

        if student_key_Level and len(student_keys) == 2:
                print(f"Search Filter: {student_key_Level}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.yearLevel LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], student_key_Level)


        # Gender constraint
        if student_key_Gender and len(student_keys) == 1:
                print(f"Search Filter: {student_key_Gender}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.gender LIKE %s) OR
                        (students.lastName LIKE %s AND students.gender LIKE %s) OR
                        (students.idNumber LIKE %s AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], student_key_Gender, student_keys[0], student_key_Gender, student_keys[0], student_key_Gender)

        if student_key_Gender and len(student_keys) == 2:
                print(f"Search Filter: {student_key_Gender}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], student_key_Gender)

        # Course Code and Year Level constraint
        if course_key_Code and student_key_Level and len(student_keys) == 1:
                print(f"Search Filter: {course_key_Code} + {student_key_Level}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.courseCode LIKE %s AND students.yearLevel LIKE %s) OR
                        (students.lastName LIKE %s AND students.courseCode LIKE %s  AND students.yearLevel LIKE %s) OR
                        (students.idNumber LIKE %s AND students.courseCode LIKE %s  AND students.yearLevel LIKE %s)'''

                SqlValues = (student_keys[0], course_key_Code, student_key_Level,
                            student_keys[0], course_key_Code, student_key_Level,
                            student_keys[0], course_key_Code, student_key_Level)

        if course_key_Code and student_key_Level and len(student_keys) == 2:
                print(f"Search Filter: {course_key_Code} + {student_key_Level}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.courseCode LIKE %s OR students.yearLevel LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], course_key_Code, student_key_Level)

        # Course Code and Gender constraint
        if course_key_Code and student_key_Gender and len(student_keys) == 1:
                print(f"Search Filter: {course_key_Code} + {student_key_Gender}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.courseCode LIKE %s AND students.gender LIKE %s) OR
                        (students.lastName LIKE %s AND students.courseCode LIKE %s  AND students.gender LIKE %s) OR
                        (students.idNumber LIKE %s AND students.courseCode LIKE %s  AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], course_key_Code, student_key_Gender,
                            student_keys[0], course_key_Code, student_key_Level,
                            student_keys[0], course_key_Code, student_key_Gender)

        if course_key_Code and student_key_Gender and len(student_keys) == 2:
                print(f"Search Filter: {course_key_Code} + {student_key_Gender}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.courseCode LIKE %s AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], course_key_Code, student_key_Gender)

       # Year Level and Gender constraint
        if student_key_Level and student_key_Gender and len(student_keys) == 1:
                print(f"Search Filter: {student_key_Level} + {student_key_Gender}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s) OR
                        (students.lastName LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s) OR
                        (students.idNumber LIKE %s AND students.yearLevel LIKE %s  AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], student_key_Level, student_key_Gender,
                            student_keys[0], student_key_Level, student_key_Gender,
                            student_keys[0], student_key_Level, student_key_Gender)

        if student_key_Level and student_key_Gender and len(student_keys) == 2:
                print(f"Search Filter: {student_key_Level} + {student_key_Gender}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], student_key_Level, student_key_Gender)

        # Course Code, Year Level, and Gender constaint
        if course_key_Code and student_key_Level and student_key_Gender and len(student_keys) == 1:
                print(f"Search Filter: {course_key_Code} + {student_key_Level} + {student_key_Gender}\nSearch Input: {student_keys[0]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.courseCode LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s) OR
                        (students.lastName LIKE %s AND students.courseCode LIKE %s AND students.yearLevel LIKE %s AND students.gender LIKE %s) OR
                        (students.idNumber LIKE %s AND students.courseCode LIKE %s AND students.yearLevel LIKE %s  AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], course_key_Code, student_key_Level, student_key_Gender,
                            student_keys[0], course_key_Code, student_key_Level, student_key_Gender,
                            student_keys[0], course_key_Code, student_key_Level, student_key_Gender)

        if course_key_Code and student_key_Level and student_key_Gender and len(student_keys) == 2:
                print(f"Search Filter: {course_key_Code} + {student_key_Level} + {student_key_Gender}\nSearch Input: {student_keys[0]} {student_keys[1]}")
                SqlQuery = '''
                        SELECT
                        students.students_id,
                        students.idNumber,
                        students.firstName,
                        students.lastName,
                        students.courseCode,
                        students.course_id,
                        students.yearLevel,
                        students.gender,
                        students.image_id,
                        COALESCE(college_table.collegeName, 'N/A') AS collegeName
                    FROM students
                    LEFT JOIN course_table
                        ON students.courseCode = course_table.courseCode
                    LEFT JOIN college_table
                        ON course_table.collegeCode = college_table.collegeCode
                    WHERE
                        (students.firstName LIKE %s AND students.lastName LIKE %s AND students.courseCode LIKE %s
                        AND students.yearLevel LIKE %s AND students.gender LIKE %s)'''
                SqlValues = (student_keys[0], student_keys[1], course_key_Code, student_key_Level, student_key_Gender)

        db = db_connection()
        cursor = db.cursor()
        cursor.execute(SqlQuery, SqlValues)
        search_data = cursor.fetchall()
        db.close()
        cursor.close()
        return search_data
