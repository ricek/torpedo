from marshmallow import Serializer, fields

class SchoolSerializer(Serializer):
    class Meta:
        fields = ("district", "number", "name", "enrollment")

class StudentSerializer(Serializer):
    class Meta:
        fields = ("osis", "lname", "fname")

class TCSerializer(Serializer):
    class Meta:
        fields = ("course_id", "section_id")
