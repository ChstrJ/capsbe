import time
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status

def format_response(data, message):
    return {
        'message': message,
        'timestamp': int(timezone.now().timestamp()),
        'data': data
    }

def response(data = None, message = None, code = status.HTTP_200_OK):
    return Response(format_response(data, message), code)
