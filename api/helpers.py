import time
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from .models import Resident
from faker import Faker

def format_response(data, message):
        
    return {
        'message': message,
        'timestamp': int(timezone.now().timestamp()),
        'data': data
    }

def response(data = None, message = None, code = status.HTTP_200_OK):
    return Response(format_response(data, message), code)

def send_fire_response(location):
    return f"Alert: Fire truck incoming on {location}. Clear the way immediately and stay alert." 

def send_medical_response(location):
    return f"Alert: Medical assistance is on the way to {location}. Please clear the area and allow emergency personnel to pass. Stay safe!" 
def send_police_response(location):
    return f"Alert: Police are responding to an incident at {location}. Please stay indoors and avoid the area for your safety."

def default_response(location):
    return f"Emergeton is on the way to {location}. Please stay calm!"

def convert_to_639(number):
    
    if number[0] == "+":
        return 
    
    return f"+639{number[2:]}"


def create_dummy_residents(count = 10):
    fake = Faker()
    data = []
    
    for _ in range(count):
        
        user_data = {
              "user": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "password": fake.password(),
              }
        }

        resident_data = {
            "contact_number": "09477936942",
            "address": fake.address(),
            "verified": False, 
            "landmark": fake.street_name(),
        }
        
        residents = {
            **user_data, 
            **resident_data
        }
        
        data.append(residents)
        
    print(data)
        
    return data