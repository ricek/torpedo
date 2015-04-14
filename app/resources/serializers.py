from flask.ext.restful import fields, reqparse

class TTP(fields.Raw):
    def format(self, value):
        return value.strftime('%H:%M')

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

entry_fields = {
    'timestamp': fields.DateTime(dt_format='rfc822'),
    'osis': fields.Integer(attribute='student_osis'),
    'status': TTP(attribute='timestamp')
}



entry_parser = reqparse.RequestParser()
entry_parser.add_argument('osis', type=int, required=True, help='Please enter student OSIS')
