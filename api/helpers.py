import time
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from .models import Resident
from faker import Faker
from datetime import datetime

def format_response(data, message):
        
    return {
        'message': message,
        'timestamp': int(timezone.now().timestamp()),
        'data': data
    }
    
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def response(data = None, message = None, code = status.HTTP_200_OK):
    return Response(format_response(data, message), code)

def send_sms_response(location, type):
    response = ''
    if type == 'fire':
        response = f"Alert: Fire truck incoming on {location}. Clear the way immediately and stay alert." 
    elif type == 'medical':
        response = f"Alert: Medical assistance is on the way to {location}. Please clear the area and allow emergency personnel to pass. Stay safe!" 
    elif type == 'police':
        response = f"Alert: Police are responding to an incident at {location}. Please stay indoors and avoid the area for your safety."
    else:
        response = f"Emergeton is on the way to {location}. Please stay calm!"
        
    return response
        

def send_email_subject(location, type):
    return f"🚨 Emergency Alert 🚨: {type.upper()} Detected at {location}, Reported: {now()}"

# def send_email_message(address, department, type, number):
#     # Initialize body as a single string
#     body = f"Dear {department},\n\n"
    
#     body += f"This is an emergency alert. A {type} has been detected at the following location:\n"
#     body += f"Location: {address}\n"
#     body += f"Date & Time: {now()}\n\n"
    
#     body += f"Immediate assistance is required. Please respond as soon as possible. For any further information or updates, contact us at {number}.\n\n"
    
#     body += "Thank you for your prompt response.\n\n"
#     body += "Best regards,\n"
#     body += "Barangay Longos Official"
    
#     return body
 
 
def send_email_message(address, department, type, number):
    # Use HTML formatting
    body = f"""
    <html>
        <body>
            <h2><strong>Dear {department},</strong></h2>
           
            <p><strong>Emergency Type: {type},</strong></p> 
            <p>This is an emergency alert. A emergency response needed at the following location:</p>
            
            <h3><strong>📍 Location:</strong> {address}<br>
            <strong>🕛 Date & Time:</strong> {now()}</h3>
            
            <p>Immediate assistance is required. Please respond as soon as possible. For any further information or updates, contact us at <strong>{number}</strong>.</p>
            
            <p>Best regards,<br>
            Barangay Longos Official</p>
        </body>
    </html>
    """
    
    return body   

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
        
        
    return data