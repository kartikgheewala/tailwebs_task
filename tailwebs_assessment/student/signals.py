from django.db.models.signals import pre_save
from django.db.models import Sum
from .models import Student


def add_marks_student(sender, instance, **kwargs):
    qry_student = Student.objects.filter(
        name=instance.name
    ).aggregate(
        Sum('marks')
    )
    print("===> qry_student: ", qry_student)

    # If this student is newly then it will not work.
    if qry_student['marks__sum'] is not None:
        qry = Student.objects.filter(
            name=instance.name
        ).update(
            total_marks=int(qry_student['marks__sum']) + int(instance.marks)
        )

    print("===> instance: ", instance.name)


pre_save.connect(add_marks_student, sender=Student)
