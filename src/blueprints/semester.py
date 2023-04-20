from flask import Blueprint

semester = Blueprint("semester", __name__,url_prefix="/mybolton/v1/semester")

@semester.get('/')
def session():
    return "Spring "