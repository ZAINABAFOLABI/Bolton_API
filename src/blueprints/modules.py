from flask import Blueprint, request, jsonify
import json
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED
import validators
# from src.config import database
from src.config.database import Module, db






modules = Blueprint("lessons", __name__,
                    url_prefix="/mybolton/v1/modules")

@modules.get('/all')
def get_all_lessons():
    return  {"Course": "SWE7101"}

@modules.post('/')
def add_new_module():
    course_title = request.json['course_title']
    course_code = request.json['course_code']

    if len(course_title)<7:
        return jsonify({
            'error': "Course title is invalid"
        }), HTTP_400_BAD_REQUEST
    
    if len(course_code)<7:
        return jsonify({
            'error': "Course code is invalid"
        }), HTTP_400_BAD_REQUEST
    if Module.query.filter_by(course_code=course_code).first() is not None:
        return jsonify({'error': "Course code already exists"}), HTTP_409_CONFLICT
    
    if Module.query.filter_by(course_title=course_title).first() is not None:
        return jsonify({'error': "Course title already exists"}), HTTP_409_CONFLICT
    
    module = Module(course_code=course_code, course_title=course_title
                      )
    db.session.add(module)
    db.session.commit()
    return jsonify({
        'message': "Module creation complete",
        'module' : {
        'Course Id': course_code,
        'Course Title': course_title,
       
        }
    }), HTTP_201_CREATED
    

