from flask import g
from flask.ext import restful
from .serializers import SchoolSerializer, StudentSerializer, TCSerializer
from . import resource
from .. import db, api, auth
from ..models import School, Student, Course

@resource.route('/')
def index():
	return '<h1>Flask is Running!</h1>'

class HelloWorld(restful.Resource):
    def get(self, name):
        return {'hello': name}

class getDBN(restful.Resource):
	def get(self, district, number=None):
		if number is None:
			schools = School.query.filter_by(district=district).all()
			return SchoolSerializer(schools, many=True).data, 201
		else:
			school = db.session.query(School).filter(School.district==district).filter(School.number==number).first()
			return SchoolSerializer(school).data, 201

class getStudents(restful.Resource):
	def get(self, district, number):
		students = Student.query.all()
		return StudentSerializer(students, many=True).data, 201

class getTeacherCourses(restful.Resource):
	@auth.login_required
	def get(self):
		course_list = db.session.query(Course.course_id, Course.section_id).distinct()
		courses = course_list.filter_by(teacher=g.current_user.lname).all()
		return TCSerializer(courses, many=True).data, 201


api.add_resource(HelloWorld, '/hello/<name>')
api.add_resource(getDBN, '/<district>', '/<district>/<number>')
api.add_resource(getStudents, '/<district>/<number>/students')
api.add_resource(getTeacherCourses, '/courses')
