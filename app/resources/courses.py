from flask.ext import restful
from flask.ext.restful import marshal_with
from .serializers import *
from .. import api
from ..models import Course

class CourseList(restful.Resource):
    @marshal_with(course_fields)
    def get(self):
        query = Course.query.all()
        return query, 200

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

class CourseByDepartment(restful.Resource):
    @marshal_with(course_fields)
    def get(self, name):
        query = Course.query.filter_by(department=name).all()
        return query, 200

api.add_resource(CourseList, '/courses')
api.add_resource(CourseByCode, '/courses/<code>')
api.add_resource(CourseBySection, '/courses/<code>/<section>')
api.add_resource(CourseByDepartment, '/courses/dept/<name>')
