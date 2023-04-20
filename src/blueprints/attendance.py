from flask import Blueprint

attendance = Blueprint("attendance", __name__,url_prefix="/mybolton/v1/attendance")

@attendance.get('/')
def attendance_log():
    return "All students present "