import time
from django.utils import timezone
from rest_framework.response import Response

def format_response(data, status):
    return {
        'message': status,
        'timestamp': int(timezone.now().timestamp()),
        'data': data
    }

def response(data, status): 
    return Response(format_response(data, status))
