from flask.ext import restful
from flask.ext.restful import marshal_with
from .serializers import *
from .. import api
from ..models import Teacher

class TeacherCourses(restful.Resource):
    @marshal_with(course_fields)
    def get(self, id):
        query = Teacher.query.filter_by(id=id.upper()).first().courses
        return query , 404

api.add_resource(TeacherCourses, '/teachers/<id>/courses')
