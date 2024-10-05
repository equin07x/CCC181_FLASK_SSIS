
/*DROP DATABASE flask_ssis;*/
CREATE DATABASE flask_ssis;
USE flask_ssis;

SELECT * FROM students;
SELECT * FROM course_table;
SELECT * FROM college_table;

DELETE FROM college_table WHERE collegeCode = "CCS";

INSERT INTO course_table(college_id, courseCode, courseName, collegeCode)
VALUES ('10', 'BSCA', 'Bachelor of Science in Computer Applications', 'CCS');

DELETE FROM course_table WHERE college_id = "10";

INSERT INTO college_table(collegeCode, collegeName)
VALUES ("CCS","College of Computer Studies");

SELECT * FROM college_table WHERE collegeCode = "CCS" AND collegeName = "College of Computer Studies";

CREATE TABLE college_table(
	college_id INT AUTO_INCREMENT UNIQUE NOT NULL,
    collegeCode VARCHAR(100),
    collegeName VARCHAR(100),
    PRIMARY KEY (college_id)
    );
    
CREATE TABLE course_table(
	course_id INT AUTO_INCREMENT UNIQUE NOT NULL,
	college_id INT,
    courseCode VARCHAR(100),
    courseName VARCHAR(100),
	collegeCode VARCHAR(100),
    PRIMARY KEY (course_id),
    FOREIGN KEY (college_id) REFERENCES college_table(college_id)
    );
    
CREATE TABLE students(
	students_id INT AUTO_INCREMENT UNIQUE NOT NULL,
    idNumber VARCHAR(20),
    firstName VARCHAR(150),
    lastName VARCHAR(150),
    courseCode VARCHAR(100),
	course_id INT,
    yearLevel VARCHAR(20),
    gender VARCHAR(20),
    PRIMARY KEY (students_id),
    FOREIGN KEY (course_id) REFERENCES course_table(course_id)
    );

DELETE FROM students where id=1;
DELETE FROM course_table where id=1;

INSERT INTO college_table(collegeCode, collegeName)
VALUES ("CCS","College of Computer Studies"),
		("CASS","College of Arts and Social Sciences"),
		("CSM","College of Science and Mathematics");

DELETE FROM `college_table` WHERE `id` = 3;
        
INSERT INTO course_table(courseCode, courseName, collegeCode)
VALUES ("BSN", "Bachelor of Science in Nursing", "CHS");

SELECT * FROM course_table;

INSERT INTO course_table (courseCode, courseName, collegeCode)
VALUES
		("BSCA","Bachelor of Science in Computer Applications", "CCS");

ALTER TABLE course_table
MODIFY courseCode VARCHAR(200) UNIQUE;

ALTER TABLE college_table
MODIFY collegeCode VARCHAR(100) UNIQUE;

ALTER TABLE students
MODIFY yearLevel varchar(20);

INSERT INTO students(idNumber, firstName, lastName, courseCode, yearLevel, gender) 
VALUES( "2022-1684", "Abdallah", "Ibrahim", "BSCS", "3rd-Year", "Male"),
	( "2212-1692", "Jeff", "Bezos", "BSMATH", "4th-Year", "Male"),
    ( "2469-1271", "Elon", "Musk", "BSCpE", "2nd-Year", "Male"),
    ( "2015-0021", "Ada", "Lovelace", "BSIT", "2nd-Year", "Female"),
    ( "2013-2012", "Margaret", "Rothschild", "BSCA", "3rd-Year", "Female"),
    ( "2002-1007", "Mark", "Zuckerberg", "BSCS", "3rd-Year", "Male"),
    ( "2042-0069", "Jimmy", "Donaldson", "BSMATH", "4th-Year", "Male"),
    ( "2016-0421", "Sophie", "Burmingham", "BSN", "2nd-Year", "Female"),
    ( "1985-0171", "Donald", "Knuth", "BSCS", "4th-Year", "Male"),
    ( "2032-1811", "Royce", "Dupont", "BSA", "4th-Year", "Male");

DELETE FROM students WHERE `students_id` = "1";
DELETE FROM college_table WHERE `collegeCode` = "CASS";
DELETE FROM course_table WHERE `course_id` = "4";

UPDATE college_table SET collegeCode = "CED", collegeName = "College of Education" WHERE college_id = "15";
UPDATE course_table SET collegeCode = "CCS" WHERE collegeCode = "N/A";