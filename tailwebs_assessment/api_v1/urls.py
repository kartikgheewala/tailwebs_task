from django.urls import path
from api_v1.views import (
    student_detail_update
)

urlpatterns = [
    path('student/edit/<int:pk>', student_detail_update, name='student_detail_update'),
    path('student/delete/<int:pk>', student_detail_update),
]
