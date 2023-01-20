import json
import requests
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
from authentication.models import (
    User
)
from .models import (
    Subject, Student
)
from authentication.decorators import (
    login_required
)


# Define subject functions
def subject(request):
    """
    :param request: GET
    :return: render the html page
    """
    if request.method == 'GET':
        return render(request, 'backend/subject.html')


@login_required
def subject_datatable(request):
    """
    :param request: GET
    :return: JsonResponse of all subjects
    """
    start = request.GET['start']
    length = request.GET['length']
    end = int(start) + int(length)
    search_value = request.GET['search[value]']
    order_column_number = request.GET['order[0][column]']
    order_column_name = request.GET['columns[' + order_column_number + '][data]']
    order_value = request.GET['order[0][dir]']
    order_sign = '-' + order_column_name

    if order_value == 'asc':
        order_sign = order_column_name

    if search_value == '':
        qry = Subject.objects.all().order_by(
            order_sign
        ).values(
            'id', 'name', 'created_at', 'updated_at'
        )
    else:
        qry = Subject.objects.filter(
            Q(id__icontains=search_value) |
            Q(name__icontains=search_value) |
            Q(created_at__icontains=search_value) |
            Q(updated_at__icontains=search_value)
        ).order_by(
            order_sign
        ).values(
            'id', 'name', 'created_at', 'updated_at'
        )

    context = {
        'data': list(qry[int(start):end]),
        'recordsTotal': len(qry),
        'recordsFiltered': len(qry)
    }

    return JsonResponse(context)


@csrf_exempt
@login_required
def get_subject_ajax(request):
    """
    :param request: POST
    :return: JSONResponse of specific subject details
    """
    if request.method == 'POST':
        qry = Subject.objects.filter(
            id=request.POST['id']
        ).first()

        data = {
            'id': qry.id,
            'name': qry.name,
        }

        return JsonResponse(data, safe=False)


@login_required
def add_subject(request):
    """
    :param request: POST
    :return: redirect
    function : Create Subject
    """
    if request.method == "POST":
        if not Subject.objects.filter(
                name=request.POST['add_name']
        ):
            Subject.objects.create(
                name=request.POST['add_name']
            )
            messages.success(request, "Record added successfully!")
        else:
            messages.error(request, "Record is already exist!")

    return redirect("/subject")


@csrf_exempt
@login_required
def edit_subject(request):
    """
    :param request: POST
    :return: redirect
    :function: Edit Subject
    """
    if request.method == "POST":
        Subject.objects.filter(
            id=request.POST['edit_id']
        ).update(
            name=request.POST['edit_name']
        )

        messages.success(request, "Record updated successfully!")

    return redirect("/subject")


@login_required
def delete_subject(request):
    """
    :param request: POST
    :return: redirect
    :function: Delete Subject
    """
    if request.method == "POST":
        Subject.objects.filter(id=request.POST['delete_id']).delete()
        messages.success(request, "Record deleted successfully!")

    return redirect("/subject")


# Define student functions
def student(request):
    """
    :param request: GET
    :return: render the html page
    """
    if request.method == 'GET':
        qry_subject = Subject.objects.all()

        context = {
            "All_Subject": qry_subject
        }
        return render(request, 'backend/student.html', context)


@login_required
def student_datatable(request):
    """
    :param request: GET
    :return: JsonResponse of all students
    """
    start = request.GET['start']
    length = request.GET['length']
    end = int(start) + int(length)
    search_value = request.GET['search[value]']
    order_column_number = request.GET['order[0][column]']
    order_column_name = request.GET['columns[' + order_column_number + '][data]']
    order_value = request.GET['order[0][dir]']
    order_sign = '-' + order_column_name

    if order_value == 'asc':
        order_sign = order_column_name

    if search_value == '':
        qry = Student.objects.filter(
            created_by=request.session['user']
        ).order_by(
            order_sign
        ).values(
            'id', 'name', 'subject__name', 'marks', 'created_at', 'updated_at'
        )
    else:
        qry = Student.objects.filter(
            Q(id__icontains=search_value) |
            Q(name__icontains=search_value) |
            Q(subject__name__icontains=search_value) |
            Q(marks__icontains=search_value) |
            Q(created_at__icontains=search_value) |
            Q(updated_at__icontains=search_value),
            created_by=request.session['user']
        ).order_by(
            order_sign
        ).values(
            'id', 'name', 'subject__name', 'marks', 'created_at', 'updated_at'
        )

    context = {
        'data': list(qry[int(start):end]),
        'recordsTotal': len(qry),
        'recordsFiltered': len(qry)
    }

    return JsonResponse(context)


@csrf_exempt
@login_required
def get_student_ajax(request):
    """
    :param request: POST
    :return: JSONResponse of specific student details
    """
    if request.method == 'POST':
        qry = Student.objects.filter(
            id=request.POST['id']
        ).first()

        data = {
            'id': qry.id,
            'name': qry.name,
            'subject_name': qry.subject_id,
            'marks': qry.marks,
        }
        return JsonResponse(data, safe=False)


@login_required
def add_student(request):
    """
    :param request: POST
    :return: redirect
    function : Create student
    """
    if request.method == "POST":
        if not Student.objects.filter(
                name=request.POST['add_name'],
                subject=request.POST['add_subject_name']
        ):
            Student.objects.create(
                name=request.POST['add_name'],
                subject=Subject.objects.get(
                    id=request.POST['add_subject_name']
                ),
                marks=request.POST['add_marks'],
                created_by=User.objects.get(
                    id=request.session['user']
                )
            )
            messages.success(request, "Record added successfully!")
        else:
            qry_student = Student.objects.get(
                name=request.POST['add_name'],
                subject=request.POST['add_subject_name']
            )
            qry_student.marks += int(request.POST['add_marks'])
            qry_student.save()

            messages.success(request, qry_student.name + " record is updated!")

    return redirect("/student")


@csrf_exempt
@login_required
def edit_student(request):
    """
    :param request: POST
    :return: redirect
    :function: Edit student
    """
    if request.method == "POST":
        qry_user = User.objects.get(
            id=request.session['user']
        )

        url = "http://127.0.0.1:8000/api/v1/student/edit/" + request.POST['edit_id']

        payload = {
            'name': request.POST['edit_name'],
            'subject': request.POST['edit_subject_name'],
            'marks': request.POST['edit_marks']
        }
        files = []

        headers = {
            'Authorization': qry_user.token,
            'Cookie': 'csrftoken=i1AubGpJcODwtJvMKuqQv8M8bNEBZ1Bl'
        }

        response = requests.request(
            "PUT", url, headers=headers, data=payload, files=files
        )

        rsp = json.loads(response.text)

        if rsp['status'] is False:
            messages.error(request, rsp['message'])
        else:
            messages.success(request, "Record updated successfully!")

    return redirect("/student")


@login_required
def delete_student(request):
    """
    :param request: POST
    :return: redirect
    :function: Delete student
    """
    if request.method == "POST":
        Student.objects.filter(id=request.POST['delete_id']).delete()
        messages.success(request, "Record deleted successfully!")

    return redirect("/student")
