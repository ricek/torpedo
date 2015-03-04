import csv
from itertools import islice
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key = True)
    district = db.Column(db.Integer)
    borough = db.Column(db.String(64))
    number = db.Column(db.Integer)
    name = db.Column(db.String(128))
    enrollment = db.Column(db.Integer)

    @staticmethod
    def insert_schools():
        with open('data\HSDBN.csv') as csvfile:
            spamreader =  islice(csv.reader(csvfile), 1, None)
            for row in spamreader:
                school = School(district=row[0][:2], borough=row[2],
                                number=row[0][3:],
                                name=row[1],
                                enrollment=row[3])
                db.session.add(school)
                print("%r%r added" % (school.district, school.number))
            db.session.commit()

    def __repr__(self):
        return 'schools'

class Student(db.Model):
    __tablename__ = 'students'
    osis = db.Column(db.Integer, primary_key =True)
    lname = db.Column(db.String(64))
    fname = db.Column(db.String(64))

    @staticmethod
    def insert_students():
        with open('data\students.csv') as csvfile:
            spamreader =  islice(csv.reader(csvfile), 1, None)
            for row in spamreader:
                student = Student(osis=row[0],lname=row[1],fname=row[2])
                db.session.add(student)
                print(student.lname+ " added")
            db.session.commit()

    def __repr__(self):
        return 'student'


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key = True)
    osis = db.Column(db.Integer)
    course_id = db.Column(db.String(64))
    section_id = db.Column(db.Integer)
    room = db.Column(db.String(64))
    period = db.Column(db.Integer)
    teacher = db.Column(db.String(64))

    @staticmethod
    def insert_courses():
        with open('data\courses.csv') as csvfile:
            spamreader =  islice(csv.reader(csvfile), 1, None)
            for row in spamreader:
                course = Course(osis=row[0],course_id=row[5],section_id=row[6],room=row[10],period=row[9],teacher=row[7])
                db.session.add(course)
            db.session.commit()
            print("commit")

    def __repr__(self):
        return 'course'


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True)
    osis = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.DateTime)
    course_id = db.Column(db.String(64))
    section_id = db.Column(db.Integer)

    def __repr__(self):
        return 'entry'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    lname = db.Column(db.String(64))
    fname = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.email

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
