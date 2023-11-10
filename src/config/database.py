from flask_sqlalchemy import SQLAlchemy
from enum import unique
from datetime import datetime
import random
import string


db = SQLAlchemy()

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code=db.Column(db.String(7), unique=True, nullable=False)
    course_title=db.Column(db.String(80), unique=True, nullable=False)
    created_time=db.Column(db.DateTime, default=datetime.now())
    updated_time=db.Column(db.DateTime, onupdate=datetime.now())
    # venue= db.relationship('Venue', backref="module")
    # enrollment = db.relationship('Enrollment', backref="module")
    # lecturer = db.relationship('Lecturer', backref="module")

   

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String(7), unique=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable= False)
    password = db.Column(db.String(80), nullable=False)
    # lesson_id=db.Column(db.Integer, db.ForeignKey('module.id'))


    def __repr__(self) -> str:
        return 'Lecturers>>> {self.firstName} {self.lastName}'
    

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseTitle = db.Column(db.String(80),nullable=False)
    courseId = db.Column(db.String(80), nullable=False)
    studentId = db.Column(db.String(8), nullable=False, unique=True)
    password= db.Column(db.String(80), nullable=False, unique=True)
    studentEmail = db.Column(db.String(80), nullable=False, unique=True)
    studentName= db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        return 'Attendance>>> {self.id}'
    

class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semesterId = db.Column(db.String(8), nullable=False)
    semesterName = db.Column(db.String(80), nullable=False)
    semesterCourseId = db.Column(db.String(7), unique=True, nullable=False)
    semesterCourseTitle = db.Column(db.String(7), unique=True, nullable=False)
    startDate =  db.Column(db.String(10), nullable=False)
    endDate =  db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('registrant.id'))

    def __repr__(self) -> str:
        return 'Semester>>> {self.id}'

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
    
class Registrant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registrantId = db.Column(db.String(7), unique=True, nullable=False)
    registrantFirstname = db.Column(db.String(80), nullable=False)
    registrantLastname = db.Column(db.String(80), nullable=False)
    registrantDepartment = db.Column(db.String(80), nullable=False)
    registrantEmail = db.Column(db.String(120), nullable= False, unique=True)
    password= db.Column(db.String(80), nullable=False)
    registrantCategory = db.Column(db.String(80), nullable=False)
    semester= db.relationship('Semester', backref="registrant")
    

    def __repr__(self) -> str:
        return 'Registrant >>>> {self.registrantId}'
    
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendorId =  db.Column(db.String(80), nullable=False, unique=True)
    vendorName = db.Column(db.String(80), nullable=False)
    vendorEmail = db.Column(db.String(120), nullable= False, unique=True)
    vendorAddress = db.Column(db.String(120), nullable= False)
    vendorPhone = db.Column(db.String(80), nullable=False,  unique=True)
    vendorProduct = db.Column(db.String(120), nullable= False)
    password= db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        return 'Vendor>>> {self.id}'
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self) -> str:
        return 'Category>>> {self.id}'
    

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(13), nullable = False)
    message = db.Column(db.String(1000), nullable = False)

    def __repr__(self) -> str:
        return 'Contact>>> {self.id}'

    




