from django.urls import path
from .views import *

urlpatterns = [
    # Define subject functions
    path('subject', subject, name="subject"),
    path('subject/datatable', subject_datatable, name="subject_datatable"),
    path('subject/get_data', get_subject_ajax, name="get_subject_ajax"),
    path('subject/add', add_subject, name="add_subject"),
    path('subject/edit', edit_subject, name="edit_subject"),
    path('subject/delete', delete_subject, name="delete_subject"),
    # Define student functions
    path('student', student, name="student"),
    path('student/datatable', student_datatable, name="student_datatable"),
    path('student/get_data', get_student_ajax, name="get_student_ajax"),
    path('student/add', add_student, name="add_student"),
    path('student/edit', edit_student, name="edit_student"),
    path('student/delete', delete_student, name="delete_student"),
]
