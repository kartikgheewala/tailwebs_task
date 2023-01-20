"""
    1. error_handler.py
    2. Here overwrite default Authentication error message.
    3. This file name define setting.py inside REST_FRAMEWORK variable.
"""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # override IsAuthenticated permission class exception
    if response is not None and response.data['detail'].code == "authentication_failed":
        response.data['status'] = False
        response.data['message'] = "Unauthorised user!"
        response.data['data'] = {}

        del response.data['detail']
    # del response.data['code']

    elif response is not None and response.data['detail'].code == "not_authenticated":
        response.data['status'] = False
        response.data['message'] = "Authentication credentials were not provided!"
        response.data['data'] = {}

        del response.data['detail']

    elif response is not None and response.data['detail'].code == "token_not_valid":
        response.data['status'] = False
        response.data['message'] = "Token is invalid or expired!"
        response.data['data'] = {}

        del response.data['detail']
        del response.data['code']
        del response.data['messages']

    return response
