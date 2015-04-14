import datetime
from flask.ext import restful
from flask.ext.restful import marshal_with
from .serializers import *
from .. import db, api
from ..models import Student, Entry

class EntryList(restful.Resource):
    @marshal_with(entry_fields)
    def get(self):
        query = Entry.query.all()
        return query

    def post(self):
        # osis = entry_parser.parse_args()['osis']
        args = entry_parser.parse_args()
        if Student.query.get_or_404(args.osis):
            entry = Entry(timestamp=datetime.datetime.now(), student_osis=args.osis)
            db.session.add(entry)
            db.session.commit()
            return "Entry added successfully"

class EntriesByStudent(restful.Resource):
    @marshal_with(entry_fields)
    def get(self, osis):
        '''
        if Student.query.get_or_404(osis):
            return "This student does not exist!"
        query = Entry.query.filter_by(student_osis=osis).all()
        return query
        '''
        if Student.query.get_or_404(osis):
            query = Student.query.get(osis).entries.all()
            return query

api.add_resource(EntryList, '/entries', endpoint='entries')
api.add_resource(EntryList, '/entries', endpoint='add_entry')
api.add_resource(EntriesByStudent, '/entries/<int:osis>')
