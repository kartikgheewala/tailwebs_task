from rest_framework import serializers
from student.models import (
    Student
)


# Student serializers
class StudentSerializer(serializers.ModelSerializer):
    marks = serializers.IntegerField(required=True)

    class Meta:
        model = Student
        fields = (
            'name', 'subject', 'marks'
        )
