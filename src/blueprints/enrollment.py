from flask import Blueprint

enrollment = Blueprint("enrollment", __name__,url_prefix="/mybolton/v1/enrollment")

@enrollment.get('/')
def enrollees():
    return "AFOLABI OMOLOLA ZAINAB "