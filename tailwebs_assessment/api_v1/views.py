from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from student.models import Student
from api_v1.serializer import StudentSerializer
from rest_framework.decorators import api_view


@api_view(['PUT', 'DELETE'])
def student_detail_update(request, pk):
    try:
        qry_student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        qry_message = {
            "status": False,
            "message": "The student does not exist!",
            "data": {}
        }
        return Response(qry_message, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = StudentSerializer(
            qry_student, data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            qry_message = {
                "status": True,
                "message": "The student record is updated!",
                "data": {
                    "id": pk,
                    "name": qry_student.name,
                    "subject": qry_student.subject.name,
                    "marks": qry_student.marks,
                }
            }
            return Response(qry_message, status=status.HTTP_200_OK)

        else:
            if 'name' in serializer.errors:
                if serializer.errors['name'] == ["This field is required."]:
                    message = "name field is required."
                elif serializer.errors['name'] == ["This field may not be null."]:
                    message = "name field may not be null."
                elif serializer.errors['name'] == ["Ensure this field has no more than 255 characters."]:
                    message = "Ensure name field has no more than 255 characters."
                else:
                    message = "Some unknown error is occur!"

            elif 'subject' in serializer.errors:
                if serializer.errors['subject'] == ["This field is required."]:
                    message = "subject field is required."
                elif serializer.errors['subject'] == ["This field may not be null."]:
                    message = "subject field may not be null."
                elif serializer.errors['subject'] == ["Incorrect type. Expected pk value, received str."]:
                    message = "subject field may expected a valid integer value."
                else:
                    message = "subject object does not exist."

            elif 'marks' in serializer.errors:
                if serializer.errors['marks'] == ["This field is required."]:
                    message = "marks field is required."
                elif serializer.errors['marks'] == ["A valid integer is required."]:
                    message = "marks field is required a valid integer."
                else:
                    message = "Some unknown error is occur!"
            else:
                message = "Some unknown error is occur!"

            qry_message = {
                "status": False,
                "message": message,
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        qry_student.delete()

        qry_message = {
            "status": True,
            "message": "The student record is deleted!",
            "data": {}
        }
        return Response(qry_message, status=status.HTTP_200_OK)
