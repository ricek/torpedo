import datetime
from flask.ext import restful
from flask.ext.restful import marshal_with
from .serializers import *
from .. import db, api
from ..period import convertTS
from ..models import Student, Entry, Course

class EntryList(restful.Resource):
    @marshal_with(entry_fields)
    def get(self):
        query = Entry.query.all()
        return query, 200

    def post(self):
        # osis = entry_parser.parse_args()['osis']
        args = entry_parser.parse_args()
        if Student.query.get_or_404(args.osis):
            entry = Entry(timestamp=datetime.datetime.now(), room=args.room, student_osis=args.osis)
            db.session.add(entry)
            db.session.commit()
            return "Entry added successfully", 200

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
            return query, 200

class EntriesByPdRm(restful.Resource):
    @marshal_with(entry_fields)
    def get(self, room, period):
        query = []
        entries = Entry.query.filter_by(room=room).all()
        if entries is not None:
            for entry in entries:
                if convertTS(entry.timestamp) == period:
                    query.append(entry)
            return query, 200
        return 404

class EntriesByDate(restful.Resource):
    @marshal_with(entry_fields)
    def get(self, room, period, date):
        query = []
        entries = Entry.query.filter_by(room=room).all()
        if entries is not None:
            for entry in entries:
                if convertTS(entry.timestamp) == period and int(entry.timestamp.strftime('%Y%m%d')) == date:
                    query.append(entry)
            return query, 200
        return 404

api.add_resource(EntryList, '/entries', endpoint='entries')
api.add_resource(EntryList, '/entries', endpoint='add_entry')
api.add_resource(EntriesByStudent, '/entries/<int:osis>')
api.add_resource(EntriesByPdRm, '/entries/<room>/<int:period>', endpoint='entries_by_pdrm')
api.add_resource(EntriesByDate, '/entries/<room>/<int:period>/<int:date>', endpoint='entries_by_date')
