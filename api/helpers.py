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

def send_firetuck_response(location):
    return f"Alert: Fire truck incoming on {location}. Clear the way immediately and stay alert." 

def send_medical_response(location):
    return f"Alert: Medical assistance is on the way to {location}. Please clear the area and allow emergency personnel to pass. Stay safe!" 
def send_police_response(location):
    return f"Alert: Police are responding to an incident at {location}. Please stay indoors and avoid the area for your safety."

def default_response(location):
    return f"Emergeton is on the way to {location}. Please stay calm!"

def convert_to_639(number):
    
    return f"+639{number[2:]}"