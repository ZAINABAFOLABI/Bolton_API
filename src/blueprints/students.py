from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED
import validators
from src.config.database import Student
from src.config.database import db
students = Blueprint("students",__name__,
                 url_prefix="/mybolton/v1/students")

@students.get('/all')
def get_all_students():
    return  {"name": "Afolabi Omolola Zainab"}

@students.post('/create')
def add_new_student():
    studentId = request.json['studentId']
    studentEmail = request.json['studentEmail']
    studentFirstname = request.json['studentFirstname']
    studentLastname = request.json['studentLastname']
    studentDepartment = request.json['studentDepartment']
    studentCategory = request.json['studentCategory']

    if len(studentId)<7 :
        return jsonify({'error':"student id is incorrect"
                        }), HTTP_400_BAD_REQUEST
    
    if len(studentFirstname)<3 :
        return jsonify({'error':"First name is too short"
                        }), HTTP_400_BAD_REQUEST
    if len(studentCategory)<4:
        return jsonify({'error': "Student category is incorrect"
                        }), HTTP_400_BAD_REQUEST
    
    if len(studentLastname)<3 :
        return jsonify({'error':"Last name is too short"
                        }), HTTP_400_BAD_REQUEST
    
    if not validators.email(studentEmail) or " " in studentEmail:
        return jsonify({'error': "Student email is invalid"}), HTTP_400_BAD_REQUEST

    if len(studentDepartment)<3:
        return jsonify({'error': "Student department is incorrect"}) , HTTP_400_BAD_REQUEST
    
    if Student.query.filter_by(studentEmail=studentEmail).first() is not None:
        return jsonify({'error': "Student email already exists"}), HTTP_409_CONFLICT
    
    if Student.query.filter_by(studentId=studentId).first() is not None:
        return jsonify({'error': "Student Id already exists"}), HTTP_409_CONFLICT
    
    student = Student(studentId=studentId, studentFirstname=studentFirstname
                      ,studentLastname=studentLastname, studentEmail=studentEmail,
                      studentDepartment=studentDepartment, studentCategory=studentCategory)
    db.session.add(student)
    db.session.commit()

    return jsonify({
        'message': "Student creation complete",
        'student' : {
        'Student Id': studentId,
        'Student firstname': studentFirstname,
        'Student lastname': studentLastname,
        'Student email': studentEmail,
        'Student department': studentDepartment,
        'Student category': studentCategory
        }
    }), HTTP_201_CREATED

    # return {"student Id": "2211467"}
