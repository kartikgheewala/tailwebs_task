from django.shortcuts import redirect


def login_required(function):
    def _function(request, *args, **kwargs):
        if "user" not in request.session:
            return redirect('/')
        else:
            return function(request, *args, **kwargs)

    return _function
