from flask_restful import fields

student_fields = {
    'osis': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'offclass': fields.String,
    'grade': fields.String
}

course_fields = {
    'code': fields.String,
    'section': fields.Integer,
    'title': fields.String,
    'department': fields.String,
    'room': fields.String,
    'period': fields.Integer
}
