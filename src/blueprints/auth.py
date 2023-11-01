from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORISED, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_201_CREATED
import validators
from src.config.database import Lecturer, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

auth = Blueprint("auth",__name__,
                 url_prefix="/mybolton/v1/auth")



@auth.post('/register')
def register():
    userId = request.json['userId']
    email = request.json['email']
    password = request.json['password']
    firstName = request.json['firstName']
    lastName = request.json['lastName']

    if len(firstName)<3:
        return jsonify({'error': "First name is too short"}), HTTP_400_BAD_REQUEST
    
    if len(lastName)<3:
        return jsonify({'error': "Last name is too short"}), HTTP_400_BAD_REQUEST
    
    if len(password)<8:
        return ({
            'error': "password is too short"
        }), HTTP_400_BAD_REQUEST
    
    if len(email)<13:
        return ({
            'error': "Email is incorrect"
        }), HTTP_400_BAD_REQUEST
    
    if len(userId)<7:
        return ({
            'error': "UserId is incorrect"
        }), HTTP_400_BAD_REQUEST
    
    # if userId.isalnum() or " " in userId:
    #     return jsonify({'error': "UserId must be numbers only"
    #                     }), HTTP_400_BAD_REQUEST
    
    if  not validators.email(email) or " " in email:
        return jsonify({'error': " Email is invalid"}), HTTP_400_BAD_REQUEST
    
    if Lecturer.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email already exists"}), HTTP_409_CONFLICT
    
    if Lecturer.query.filter_by(userId=userId).first() is not None:
        return jsonify({'error': "UserId already exists"}), HTTP_409_CONFLICT
    
    pwd_hash = generate_password_hash(password)
    lecturer = Lecturer(userId=userId, firstName=firstName,
                        lastName=lastName, email=email, password=pwd_hash)

    db.session.add(lecturer)
    db.session.commit()

    return jsonify({
        'message':"Succesfully registered lecturer",
        'lecturer': {
            'firstName':firstName, "userId": userId, "lastName": lastName, "email": email
        
        
                    }}), HTTP_201_CREATED

    # return "Welcome Omolola"

@auth.post('/login')
def login():
    email = request.json.get('email', ' ')
    password = request.json.get('password', ' ')

    lecturer=Lecturer.query.filter_by(email=email).first()
    if lecturer:
        is_pass_correct= check_password_hash(lecturer.password,password)
        if is_pass_correct:
            refresh=create_refresh_token(identity=lecturer.id)
            access=create_access_token(identity=lecturer.id)

            return jsonify({
                'lecturer':{
                'refresh':refresh,
                'access':access,
                'firstName':lecturer.firstName,
                'lastName': lecturer.lastName,
                'email':lecturer.email
                }
            }),HTTP_200_OK
    return jsonify({'error': "Wrong credentials"}), HTTP_401_UNAUTHORISED


@auth.get("/lecturer")
@jwt_required()
def lecturer():
    lecturer_id= get_jwt_identity()
    lecturer= Lecturer.query.filter_by(id=lecturer_id).first()
    return jsonify({
        'firstName': lecturer.firstName,
        'lastName':lecturer.lastName,
        'email':lecturer.email,
    

    })
    import pdb
    pdb.set_trace()
    return {"user": "me"}

