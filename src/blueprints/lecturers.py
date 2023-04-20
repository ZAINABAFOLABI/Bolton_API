from flask import Blueprint

lecturers = Blueprint("lecturers", __name__, url_prefix="/mybolton/v1/lecturers")

@lecturers.get('/')
def tutor():
    return {"lecturer": "Dame Zainab"}