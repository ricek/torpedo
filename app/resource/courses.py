from flask.ext import restful
from flask_restful import marshal_with
from .serializers import *
from .. import api
from ..models import Course

class DepartmentCourses(restful.Resource):
    @marshal_with(course_fields, envelope='courses')
    def get(self, name):
        query = Course.query.filter_by(department=name).all()
        return query , 404

api.add_resource(DepartmentCourses, '/courses/departments/<name>')
