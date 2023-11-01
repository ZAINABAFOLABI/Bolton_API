from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_405_METHOD_NOT_ALLOWED
from src.config.database import db, Semester
import validators
from datetime import date
semester = Blueprint("semester", __name__,url_prefix="/mybolton/v1/semester")

@semester.route('/', methods=['POST','GET'])
def session():
    if request.method == 'POST':
        semesterId = request.get_json().get('semesterId', ' ')
        semesterName = request.get_json().get('semesterName', ' ')
        semesterCourseId = request.get_json().get('semesterCourseId', ' ')
        semesterCourseTitle = request.get_json().get('semesterCourseTitle', ' ')
        startDate = request.get_json().get('startDate', ' ')
        endDate = request.get_json().get('endDate', ' ')

        if Semester.query.filter_by(semesterCourseId=semesterCourseId).first() is not None:
            return jsonify({
                'error': " Duplicate course Id is not allowed"
            }), HTTP_400_BAD_REQUEST
        
        if Semester.query.filter_by(semesterCourseTitle= semesterCourseTitle).first() is not None:
            return jsonify({
                'error': "Duplicate course title is not allowed"
            }), HTTP_400_BAD_REQUEST
        
        if len(semesterCourseId)<7:
            return jsonify({
                'error': "Invalid Course id"
            }), HTTP_400_BAD_REQUEST
        
        if len(semesterCourseTitle)<3:
            return jsonify({
                'error': "Invalid course title"
            }), HTTP_400_BAD_REQUEST
        if len(semesterId)<4:
            return jsonify({
                'error': "Semester Id is invalid"
            }), HTTP_400_BAD_REQUEST
        
        if len(semesterName)<4:
            return jsonify({
                'error': "Invalid semester name"
            }), HTTP_400_BAD_REQUEST
        
        
        if len(startDate)<7:
            return jsonify({
                'error': "Invalid start date"
            }), HTTP_400_BAD_REQUEST
        
        if len(endDate)<7:
            return jsonify({
                'error': " Invalid end date"
            }), HTTP_400_BAD_REQUEST
        
        if len(startDate)>10:
            return jsonify({
                'error': "Invalid start date"
            }), HTTP_400_BAD_REQUEST
        
        if len(endDate)>10:
            return jsonify({
                'error': " Invalid end date"
            }), HTTP_400_BAD_REQUEST
        # if startDate > endDate:
        #     return jsonify({
        #         'error': "Invalid start and end date, start date must be earlier than end date"
        #     }), HTTP_400_BAD_REQUEST
        
        # if endDate > startDate:
        #     return jsonify({
        #         'error': "Invalid start and end date, end date must be later than start date"
        #     }), HTTP_400_BAD_REQUEST
        
        availableSession = Semester(semesterId=semesterId, semesterName=semesterName,
                                    semesterCourseId=semesterCourseId, semesterCourseTitle=semesterCourseTitle,
                                    startDate=startDate, endDate=endDate)
        db.session.add(availableSession)
        db.session.commit()   

        return jsonify({
            'semesterId': semesterId,
            'semesterName': semesterName,
            'courseId': semesterCourseId,
            'courseTitle': semesterCourseTitle,
            'startDate': startDate,
            'endDate': endDate
        })
    else:
        availableSessions = Semester.query.filter_by().all()
        data=[]
        for session in availableSessions:
            data.append({
                'semesterId': session.semesterId,                
                'semesterName': session.semesterName,
                'courseId': session.semesterCourseId,
                'courseTitle': session.semesterCourseTitle,
                'startDate': session.startDate,
                'endDate': session.endDate
            })

        return jsonify({'data':data}), HTTP_200_OK
    
@semester.delete('/delete/<semesterCourseId>')
def delete_semeter_record(semesterCourseId):
    if Semester.query.filter_by(semesterCourseId=semesterCourseId).first() is None:
        return jsonify({
            "error": "Course Id does not exist"
        }), HTTP_400_BAD_REQUEST
    Semester.query.filter_by(semesterCourseId=semesterCourseId).delete()
    db.session.commit()
    return {"Course module deleted" : f"semesterCourseId: {semesterCourseId}"}, HTTP_200_OK
    
@semester.get("/<semesterId>")
def selectedSemester(semesterId):
    currentSemester = Semester.query.filter_by(semesterId=semesterId).all()
    data =[]
    for current in currentSemester:
        data.append({
                'semesteId': current.semesterId,                
                'semesterName': current.semesterName,
                'courseId': current.semesterCourseId,
                'courseTitle': current.semesterCourseTitle,
                'startDate': current.startDate,
                'endDate': current.endDate
        })
    return jsonify ({'data':data}), HTTP_200_OK



        
    return "Spring "