from flask_sqlalchemy import SQLAlchemy
from enum import unique
from datetime import datetime
import random
import string


db = SQLAlchemy()

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code=db.Column(db.String(7), unique=True, nullable=False)
    course_title=db.Column(db.Text(80), unique=True, nullable=False)
    created_time=db.Column(db.DateTime, default=datetime.now())
    updated_time=db.Column(db.DateTime, onupdate=datetime.now())
    venue= db.relationship('Venue', backref="module")
    enrollment = db.relationship('Enrollment', backref="module")
    lecturer = db.relationship('Lecturer', backref="module")

   

    def __repr__(self) -> str:
        return 'Lesson>>>> {self.id}'
    

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), nullable=False)
    start_time =db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    course_id= db.Column(db.Integer,db.ForeignKey('module.id'))


    def __repr__(self) -> str:
        return 'Venue>>>> {self.location}'


class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable= False)
    lesson_id=db.Column(db.Integer, db.ForeignKey('module.id'))


    def __repr__(self) -> str:
        return 'Lecturers>>> {self.first_name} {self.last_name}'
    

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_code = db.Column(db.String(6), nullable=False)

    def generate_checkin_code(self):
        characters=string.ascii_letters_uppercase
        picked_chars= ' '.join(random.choices(characters, k=6))

        code=self.query.filter_by(check_in_code=picked_chars).first()

        if code:
            self.generate_checkin_code()
            # pass
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.check_in_code = self.generate_checkin_code()

    def __repr__(self) -> str:
        return 'Attendance>>> {self.id}'
    
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer,db.ForeignKey('module.id'))

    def __repr__(self) -> str:
        return 'Attendance>>> {self.id}'
    

class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        return 'Attendance>>> {self.id}'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentId = db.Column(db.String(80), unique=True, nullable=False)
    studentFirstname = db.Column(db.String(80), nullable=False)
    studentLastname = db.Column(db.String(80), nullable=False)
    studentDepartment = db.Column(db.String(80), nullable=False)
    studentEmail= db.Column(db.String(120), unique=True, nullable=False)
    studentCategory = db.Column(db.String(80), nullable = False)

    def __repr__(self) -> str:
        return 'Students>>> {self.id}'


