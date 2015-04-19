from flask.ext.restful import fields, reqparse
from ..period import entryStatus, convertTS

class getTS(fields.Raw):
    def format(self, value):
        return entryStatus(value)

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
    'status': getTS(attribute='timestamp',default='Absent')
}

entry_parser = reqparse.RequestParser()
entry_parser.add_argument('osis', type=int, required=True, help='Please enter student OSIS')
entry_parser.add_argument('room', type=str, required=True, help='Please enter room as a string')
