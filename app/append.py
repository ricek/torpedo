import os, csv
from itertools import islice
from . import db
from .models import Student, Course

def appendStudents():
    cr101, headers = urlretrieve(os.getenv('CR1_01'))
    with open(cr101) as csvfile:
        spamreader =  islice(csv.reader(csvfile), 1, None)
        for row in spamreader:
            student = Student.query.get(row[0])
            course = Course.query.filter_by(code=row[5]).filter_by(section=row[6]).first()
            course.students.append(student)
        db.session.commit()
        print("All students added to matching course!")
