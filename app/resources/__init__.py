from flask import Blueprint

resources = Blueprint('resources', __name__)

from . import students, courses, teachers, entries

@resources.route('/v1')
def index():
    return "torpedo api v1 (beta v0.1)"
