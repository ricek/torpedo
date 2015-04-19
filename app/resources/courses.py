from flask.ext import restful
from flask.ext.restful import marshal_with
from .serializers import *
from .. import api
from ..models import Course
from ..decorators import collection

@collection(Course)
def filter():
    return Course.query

class CourseList(restful.Resource):
    @marshal_with(course_fields)
    def get(self):
        query = filter()
        if query is None:
            return Course.query.all()
        elif query.count() == 1:
            return query.first()
        return query.all(), 200

class CourseByCode(restful.Resource):
    @marshal_with(course_fields)
    def get(self, code):
        query = Course.query.filter_by(code=code.upper()).all()
        return query, 200

class CourseBySection(restful.Resource):
    @marshal_with(course_fields)
    def get(self, code, section):
        query = Course.query.filter_by(code=code.upper()).filter_by(section=section).first()
        return query, 200

class StudentByCS(restful.Resource):
    @marshal_with(student_fields)
    def get(self, code, section):
        course = Course.query.filter_by(code=code.upper()).filter_by(section=section).first()
        query = course.students
        return query, 200

class CourseByDepartment(restful.Resource):
    @marshal_with(course_fields)
    def get(self, name):
        query = Course.query.filter_by(department=name).all()
        return query, 200

api.add_resource(CourseList, '/courses/')
api.add_resource(CourseByCode, '/courses/<code>')
api.add_resource(CourseBySection, '/courses/<code>/<section>')
api.add_resource(StudentByCS, '/courses/<code>/<section>/students')
api.add_resource(CourseByDepartment, '/courses/dept/<name>')
