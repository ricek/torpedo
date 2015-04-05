from flask.ext import restful
from flask_restful import marshal_with
from .serializers import *
from .. import api
from ..models import Student

class StudentList(restful.Resource):
    @marshal_with(student_fields, envelope='students')
    def get(self):
        query = Student.query.all()
        return query , 404

class StudentInfo(restful.Resource):
    @marshal_with(student_fields, envelope='student')
    def get(self, osis):
        query = Student.query.filter_by(osis=osis).first()
        return query , 404

class StudentCourses(restful.Resource):
    @marshal_with(course_fields, envelope='courses')
    def get(self, osis):
        query = Student.query.filter_by(osis=osis).first().courses
        return query , 404


api.add_resource(StudentList, '/students', endpoint = 'students')
api.add_resource(StudentInfo, '/students/<int:osis>', endpoint = 'student')
api.add_resource(StudentCourses, '/students/<int:osis>/courses')
