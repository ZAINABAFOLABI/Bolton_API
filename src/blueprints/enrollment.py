from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORISED, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_201_CREATED
import validators
from src.config.database import Enrollment, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

enrollment = Blueprint("enrollment", __name__,url_prefix="/mybolton/v1/enrollment")

@enrollment.post('/register')
def enrollees():
    courseId= request.json['courseId']
    courseTitle = request.json['courseTitle']
    studentId = request.json['studentId']
    password = request.json['password']
    studentName = request.json['studentName']
    studentEmail = request.json['studentEmail']


    if len (courseId)<7:
        return jsonify({
            'error': "Course Id is invalid"
        }), HTTP_400_BAD_REQUEST
    
    if len(studentName)<3:
        return jsonify({
            'error': "Student name is too short"
        }), HTTP_400_BAD_REQUEST
    
    if len(courseTitle)<5:
        return jsonify({
            'error': "Course title is invalid"
        }), HTTP_400_BAD_REQUEST
    
    if len(studentId)<7:
        return jsonify({
            'error': "StudentId is incomplete"
        }), HTTP_400_BAD_REQUEST
    
    if len(studentEmail)<13:
        return jsonify({
            'error': "Student email is incorrect"
        }), HTTP_400_BAD_REQUEST
    
    if not validators.email(studentEmail) or " " in studentEmail:
        return jsonify ({
            'error': "Student email is invalid"

        }), HTTP_400_BAD_REQUEST
    
    if "@bolton.ac.uk" not in studentEmail:
        return jsonify({
            'error': "Invalid email, use university assigned email"
        }), HTTP_400_BAD_REQUEST
    
    if len(password)<10:
        return jsonify({
            'error': "Password must be at least 10 characters long"
        })
    
    if Enrollment.query.filter_by(studentId=studentId).first()is not None and Enrollment.query.filter_by(courseId=courseId).first() is not None:
        return jsonify({
            'error': "Multiple enrollment for same course by same student is not allowed"
        }), HTTP_409_CONFLICT
   
    
    pwd_hash = generate_password_hash(password)
    enrollment = Enrollment(studentId=studentId,studentEmail=studentEmail, password=pwd_hash,
                            courseId=courseId, courseTitle=courseTitle, studentName=studentName)
    
    db.session.add(enrollment)
    db.session.commit()

    return jsonify ({
        'message': "Enrollment Successful",
        'enrollment':{
        'studentId': studentId, "Student name": studentName, 'Course code': courseId,
        'Course title': courseTitle
        }
    }), HTTP_201_CREATED

@enrollment.post('/login')
def login():
     studentId = request.json.get('studentId', ' ')
     password = request.json.get('password', ' ')
     enrollment=Enrollment.query.filter_by(studentId=studentId).first()
     if enrollment:
         is_pass_correct=check_password_hash(enrollment.password,password)
         if is_pass_correct:
            refresh=create_refresh_token(identity=enrollment.id)
            access=create_access_token(identity=enrollment.id)
            return jsonify({
                'enrollment':{
                'refresh':refresh,
                'access':access,
                'studentName':enrollment.studentName,
                'studentId': enrollment.studentId,
                'studentEmail':enrollment.studentEmail,
                }
            }),HTTP_200_OK
     return jsonify({'error': "Wrong credentials"}), HTTP_401_UNAUTHORISED
@enrollment.get("/enrolledStudents/<courseId>")
# @jwt_required()
def enrolleeDetail(courseId):
    # courseId= get_jwt_identity()
    enrolledStudents= Enrollment.query.filter_by(courseId=courseId).all
    data= []
    for studentRecord in enrolledStudents:
        data.append({
            'studentId': studentRecord.studentId,
            'studentEmail': studentRecord.studentEmail,
            'studentName': studentRecord.studentFirstname,
   


        })
        return jsonify({'data':data}), HTTP_200_OK
    

@enrollment.route('/',methods=['POST','GET'])
@jwt_required()
def enrollStudents():
    current_user=get_jwt_identity()
    if request.method == 'POST':
        studentId=request.get_json().get('studentId', '')
        courseId=request.get_json().get('courseId', '')
        courseTitle=request.get_json().get('courseTitle', '')
        studentName=request.get_json().get('studentName', '')
        studentEmail = request.get_json().get('studentEmail', '')
        password = request.get_json().get('password', '')

        if not validators.email(studentEmail):
            return jsonify({
            'error':"Invalid student email"
            }), HTTP_400_BAD_REQUEST
        if "@bolton.ac.uk" not in studentEmail:
            return jsonify({
            'error': "Invalid email, use university assigned email"
            }), HTTP_400_BAD_REQUEST
        if len(studentId)<7:
            return jsonify({
            'error': " Student id i incorrect"
            }), HTTP_400_BAD_REQUEST
        if len (courseId)<7:
            return jsonify({
            'error': "Course Id is invalid"
            }), HTTP_400_BAD_REQUEST
    
        if len(studentName)<3:
                return jsonify({
            'error': "Student name is too short"
            }), HTTP_400_BAD_REQUEST
    
        if len(courseTitle)<5:
            return jsonify({
            'error': "Course title is invalid"
            }), HTTP_400_BAD_REQUEST
        if len(password)<10:
            return jsonify({
            'error':"Password must be at least 10 characters long"
            }), HTTP_400_BAD_REQUEST
        # if not password.isalnum() in password:
        #     return jsonify({
        #     'error':"Password must contain letters and numbers"
        #     }),HTTP_400_BAD_REQUEST
            
        if Enrollment.query.filter_by(id=id).first() is not None:
            return jsonify({
            'error': "Multiple enrollment for same course by same student is not allowed"
            }), HTTP_409_CONFLICT
            
        enrolled=Enrollment(studentId=studentId,studentName=studentName,
                                studentEmail=studentEmail,courseId=courseId,
                                courseTitle=courseTitle,password=password, user_Id=current_user)
        db.session.add(enrolled)
        db.session.commit()
        return jsonify({
                {
                'studentId':enrolled.studentId,
                'studentEmail':enrolled.studentEmail,
                'studentName':enrolled.studentName,
                'courseId':enrolled.courseId,
                'courseTitle':enrolled.courseTitle
                }}), HTTP_201_CREATED
    else:

        totalEnrollment=Enrollment.query.filter_by(id=current_user)

        data=[]
        for enrolledCourses in totalEnrollment:
            data.append({
            'studentId':enrolledCourses.studentId,
            'studentEmail':enrolledCourses.studentEmail,
            'studentName':enrolledCourses.studentName,
            'courseId':enrolledCourses.courseId,
            'courseTitle':enrolledCourses.courseTitle
            })

        return jsonify({'data':data}), HTTP_200_OK
    
@enrollment.get('/<courseId>')
def specificCourseEnrollees(courseId):
    courseEnrollees = Enrollment.query.filter_by(courseId=courseId).all()
    data=[]
    for student in courseEnrollees:
        data.append({
            'Student name': student.studentName,
            'Student Id': student.studentId,
            'Email': student.studentEmail,
            'Course Code': student.courseId,
            'Course Title': student.courseTitle
            
        })

    return jsonify({'data':data}), HTTP_200_OK 

     



    # return "AFOLABI OMOLOLA ZAINAB "