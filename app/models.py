import csv
from itertools import islice
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager

#Alternatively you can use the __tablename__ attribute to override the default naming convention used by Flask-SQLAlchemy.

students_schedule = db.Table('students_schedule', db.Model.metadata,
   db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
   db.Column('student_osis', db.Integer, db.ForeignKey('student.osis')),
)

teachers_schedule = db.Table('teachers_schedule', db.Model.metadata,
   db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
   db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
)

class Student(db.Model):
    osis = db.Column(db.Integer, primary_key =True)
    lname = db.Column(db.String(64))
    fname = db.Column(db.String(64))
    offclass = db.Column(db.String(32))
    grade = db.Column(db.Integer)

    entries = db.relationship('Entry', backref='student', lazy='dynamic')
    courses = db.relationship("Course", secondary=students_schedule)

    @staticmethod
    def insert_students():
        with open('data\cr101.csv') as csvfile:
            spamreader =  islice(csv.reader(csvfile), 1, None)
            for row in spamreader:
                if Student.query.get(row[0]) is None:
                    student = Student(osis=row[0],lname=row[1],fname=row[2],offclass=row[3],grade=row[4])
                    db.session.add(student)
            db.session.commit()
            print("All students added!")

    def __repr__(self):
        return '<%r %r %r>' % (self.osis, self.lname, self.fname[0])

class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(64))
    section = db.Column(db.Integer)
    title = db.Column(db.String(64))
    department = db.Column(db.String(64))
    period = db.Column(db.Integer)
    room = db.Column(db.String(64))

    students = db.relationship("Student", secondary=students_schedule)
    teachers = db.relationship("Teacher", secondary=teachers_schedule)

    @staticmethod
    def insert_courses():
        with open('data\cr101.csv') as csvfile:
            spamreader =  islice(csv.reader(csvfile), 1, None)
            for row in spamreader:
                if Course.query.filter_by(code=row[5]).filter_by(section=row[6]).first() is None:
                    course = Course(code=row[5],section=row[6],period=row[9],room=row[10])
                    db.session.add(course)
            db.session.commit()
            print("All courses added!")

    def __repr__(self):
        return '<%r-%r>' % (self.code, self.section)

class Teacher(db.Model):
    id = db.Column(db.String, primary_key = True)
    lname = db.Column(db.String(64))
    fname = db.Column(db.String(64))

    courses = db.relationship("Course", secondary=teachers_schedule)

    @staticmethod
    def insert_teachers():
        with open('data\demo'+'\\'+'teachers.csv') as csvfile:
            spamreader =  islice(csv.reader(csvfile), 1, None)
            for row in spamreader:
                teacher = Teacher(id=row[0],lname=row[1],fname=row[2])
                db.session.add(teacher)
            db.session.commit()
            print("All teachers added!")

    def __repr__(self):
        return '<%r %r>' % (self.lname, self.fname[0])

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime)
    room = db.Column(db.String(64))
    student_osis = db.Column(db.Integer, db.ForeignKey('student.osis'))

    def __repr__(self):
        return '<%r: %r>' % (self.timestamp, self.student_osis)


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
