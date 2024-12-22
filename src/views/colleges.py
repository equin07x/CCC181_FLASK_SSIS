from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint
import pymysql.cursors
from config import SECRET_KEY
from src.database import db_connection
#from models.courses import course_M
#from models.students import student_M



colleges_bp = Blueprint("Clbp", __name__,  template_folder='/templates')