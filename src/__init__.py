from flask import Flask
import os
from src.blueprints.auth import auth
from src.blueprints.attendance import attendance
from src.blueprints.enrollment import enrollment
from src.blueprints.lecturers import lecturers
from src.blueprints.venues import venues
from src.blueprints.modules import modules
from src.blueprints.semester import semester
from src.blueprints.students import students
from src.blueprints.vendors import vendors
from src.blueprints.contact import contact
from src.config.database import db
from flask_jwt_extended import JWTManager



def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)
    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )

    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app) 
    JWTManager(app)

    app.register_blueprint(modules)
    app.register_blueprint(auth)
    app.register_blueprint(venues)
    app.register_blueprint(semester)
    app.register_blueprint(attendance)
    app.register_blueprint(enrollment)
    app.register_blueprint(lecturers)
    app.register_blueprint(students)
    app.register_blueprint(vendors)
    app.register_blueprint(contact)

  
    return app

