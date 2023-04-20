from flask import Blueprint

auth = Blueprint("auth",__name__,
                 url_prefix="/mybolton/v1/auth")



@auth.post('/register')
def register():
    return "Welcome Omolola"

@auth.get("/me")
def me():
    return {"user": "me"}

