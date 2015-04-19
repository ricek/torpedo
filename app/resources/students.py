from flask import request
from flask.ext import restful
from flask.ext.restful import marshal_with
from .serializers import *
from .. import api
from ..models import Student
from ..decorators import collection

@collection(Student)
def filter():
    return Student.query

class StudentList(restful.Resource):
    @marshal_with(student_fields)
    def get(self):
        query = filter()
        if query is None:
            return Student.query.all()
        elif query.count() == 1:
            return query.first()
        return query.all(), 200

class StudentInfo(restful.Resource):
    @marshal_with(student_fields)
    def get(self, osis):
        query = Student.query.filter_by(osis=osis).first()
        return query, 200

class CoursesByStudent(restful.Resource):
    @marshal_with(course_fields)
    def get(self, osis):
        query = Student.query.filter_by(osis=osis).first().courses
        return query, 200

api.add_resource(StudentList, '/students/', endpoint='students')
api.add_resource(StudentInfo, '/students/<int:osis>', endpoint='student')
api.add_resource(CoursesByStudent, '/students/<int:osis>/courses')
