#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Student, Course, Entry, User, Teacher
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, Student=Student, Course=Course, Entry=Entry, User=User, Teacher=Teacher)

manager.add_command("shell", Shell(make_context=make_shell_context))

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    manager.run()