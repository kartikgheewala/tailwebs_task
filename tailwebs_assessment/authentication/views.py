from django.shortcuts import (
    render, redirect
)
from django.contrib import messages
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login as auth_login
from .models import (
    User
)
from student.models import (
    Subject, Student
)
from .decorators import (
    login_required
)


# Create your views here.
def login(request):
    if "user" in request.session:
        return redirect('/dashboard')

    elif request.method == 'GET':
        return render(request, 'auth/login.html')

    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
            auth_login(request, user)

            request.session['user'] = user.pk

            # Token Generator
            token_value = Token.objects.filter(user_id=user.pk)

            if token_value.exists():
                # Here every time new token will be generated when user login.
                token_value.delete()

                token, create = Token.objects.get_or_create(user_id=user.pk)
            else:
                token, create = Token.objects.get_or_create(user_id=user.pk)

            print(token)

            tkn = "Token " + str(token)

            user = User.objects.get(
                id=user.pk
            )
            user.token = tkn
            user.save()

            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


@login_required
def dashboard(request):
    if request.method == 'GET':
        qry_user = User.objects.all().count()

        qry_subject = Subject.objects.all().count()

        qry_student = Student.objects.filter(
            created_by=request.session['user']
        ).count()

        context = {
            "All_User": qry_user,
            "All_Subject": qry_subject,
            "All_Student": qry_student,
        }
        return render(request, 'backend/dashboard.html', context)
