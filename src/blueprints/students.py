from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_401_UNAUTHORISED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_200_OK, HTTP_201_CREATED
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from src.config.database import Student, Registrant
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.config.database import db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

students = Blueprint("students",__name__,
                 url_prefix="/mybolton/v1/students")

# Registering new intakes into the db and logging them in as well
@students.post('/register')
def register_student(): 
    registrantId = request.json['registrantId']
    registrantFirstname = request.json['registrantFirstname']
    registrantLastname = request.json['registrantLastname']
    registrantEmail = request.json['registrantEmail']
    registrantDepartment = request.json['registrantDepartment']
    password = request.json['password']
    registrantCategory = request.json['registrantCategory']

    if len(registrantId)<7:
        return jsonify({
            'error': "Id is incorrect"
        }), HTTP_400_BAD_REQUEST
    
    if Registrant.query.filter_by(registrantId=registrantId).first() is not None:
        return jsonify({
            'error': "Id already exists"
        }), HTTP_409_CONFLICT
    
    
    if len(registrantFirstname)<3:
        return jsonify({
            'error': "First name is too short"
        }), HTTP_400_BAD_REQUEST
    
    if len(registrantLastname)<3:
        return jsonify({
            'error': "Last name is too short"
        }), HTTP_400_BAD_REQUEST
    
    if not validators.email(registrantEmail):
        return jsonify({
            'error': "Invalid email"
        }), HTTP_400_BAD_REQUEST
    
    if "@bolton.ac.uk" not in registrantEmail:
        return jsonify({
            'error': "Invalid email, use University assigned email"
        }), HTTP_400_BAD_REQUEST
    
    if len(registrantDepartment)<3:
        return jsonify({
            'error': "Invalid department"
        }), HTTP_400_BAD_REQUEST
    
    if len(password)<10:
        return jsonify({
            'error': "Password must be at least 10 characters long"
        }), HTTP_400_BAD_REQUEST
    
    # if Registrant.query.filter_by(registrantId=registrantId).first() is not None:
    #     return jsonify({
    #         'error': " Multiple registration is not allowed"
    #     }), HTTP_409_CONFLICT
    
    if Registrant.query.filter_by(registrantEmail=registrantEmail).first() is not None:
        return jsonify({
            'error': "Email already exists"
        }), HTTP_409_CONFLICT
    
    if len(registrantCategory)<4:
        return jsonify({
            'error': "Wrong student category"
        }), HTTP_400_BAD_REQUEST
    
    
    pwd_hash = generate_password_hash(password)

    registeredStudent= Registrant(registrantId=registrantId, 
                                  registrantFirstname=registrantFirstname, registrantLastname=registrantLastname,
                                  registrantEmail=registrantEmail, registrantDepartment=registrantDepartment,
                                  registrantCategory=registrantCategory, password=pwd_hash)
    
    db.session.add(registeredStudent)
    db.session.commit()
    return jsonify({
        'message': "Registration successful",
        'registration':{ 'registrantId': registrantId, 'registrantFirstname': registrantFirstname,
                        'registrantLastname': registrantLastname, 'registrantEmail': registrantEmail,
                        'registrantDepartment':registrantDepartment, 'registrantCategory': registrantCategory
        
        }
    }), HTTP_201_CREATED

# Deleting a student record from the db
@students.delete('/delete/<registrantId>')
def delete_student_record(registrantId):
    # registrantId = request.json['registrantId']
    # registrantFirstname = request.json['registrantFirstname']
    # registrantLastname = request.json['registrantLastname']
    # registrantEmail = request.json['registrantEmail']
    # registrantDepartment = request.json['registrantDepartment']
    # password = request.json['password']
    # registrantCategory = request.json['registrantCategory']
    if Registrant.query.filter_by(registrantId=registrantId).first() is None:
        return jsonify({
            'error': "The student id does not exists"
        }), HTTP_400_BAD_REQUEST
    Registrant.query.filter_by(registrantId=registrantId).delete()
    # deletedStudent= Registrant(registrantId=registrantId, 
    #                               registrantFirstname=registrantFirstname, registrantLastname=registrantLastname,
    #                               registrantEmail=registrantEmail, registrantDepartment=registrantDepartment,
    #                               registrantCategory=registrantCategory, password=pwd_hash)
    # pwd_hash = generate_password_hash(password)
    # db.session.delete()
    db.session.commit()
    return {"Student record deleted" : f"registrantId: {registrantId}"}, HTTP_200_OK

    

@students.post('/login')
def login_student():
    registrantId = request.json.get('registrantId', ' ')
    password = request.json.get('password', ' ')
    studentLogin = Registrant.query.filter_by(registrantId=registrantId).first()
    if studentLogin:
        is_pass_correct = check_password_hash(studentLogin.password, password)
        if is_pass_correct:
            refresh = create_refresh_token(identity=studentLogin.id)
            access = create_access_token(identity=studentLogin.id)
            return jsonify({
                'studentLogin':{
                'refresh':refresh,
                'access':access,
                'First name':studentLogin.registrantFirstname,
                'Last name': studentLogin.registrantLastname,
                'Email':studentLogin.registrantEmail,
                }
            }),HTTP_200_OK
    return jsonify({'error': "Wrong credentials"}), HTTP_401_UNAUTHORISED

    

    




@students.get('/all')
# @jwt_required
def get_all_students():
    # students= Student.query.filter_by(studentId=studentId).all
    # data= []
    # for studentRecord in students:
    #     data.append({
    #         'studentId': studentRecord.studentId,
    #         'studentEmail': studentRecord.studentEmail,
    #         'studentFirstname': studentRecord.studentFirstname,
    #         'studentLastname': studentRecord.studentLastname,
    #         'studentDepartment': studentRecord.studentDepartment,
    #         'studentCategory': studentRecord.studentCategory


    #     })
    #     return jsonify({'data':data}), HTTP_200_OK


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
    
    # note constraint to handle if the student id contains alphabets or special character
    
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
