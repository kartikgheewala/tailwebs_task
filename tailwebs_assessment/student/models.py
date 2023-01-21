from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Sum
from authentication.models import (
    User
)


class Subject(models.Model):
    """
    Create a subject table.
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subject"
        verbose_name = "Subject"
        verbose_name_plural = "Subject"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["name"])
        ]


class Student(models.Model):
    """
    Create a student table.
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    marks = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student"
        verbose_name = "Student"
        verbose_name_plural = "Student"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["name"])
        ]
