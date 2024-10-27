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

def send_sms_response(all_data):
    
    link = f"https://www.google.com/maps/place/{all_data['latitude']},{all_data['longitude']}"
    
    if all_data['alert_type'] == 'fire':
        response = f"Alert: Fire truck incoming on {all_data['address']}. Clear the way immediately and stay alert.\n" 
        response += f"Google Maps Link: {link}"
    elif all_data['alert_type'] == 'medical':
        response = f"Alert: Medical assistance is on the way to {all_data['address']}. Please clear the area and allow emergency personnel to pass. Stay safe!" 
        response += f"Google Maps Link: {link}"
    elif all_data['alert_type'] == 'police':
        response = f"Alert: Police are responding to an incident at {all_data['address']}. Please stay indoors and avoid the area for your safety."
        response += f"Google Maps Link: {link}"
    else:
        response = f"Emergeton is on the way to {all_data['address']}. Please stay calm!"
        response += f"Google Maps Link: {link}"
        
        
    return response
        

def send_email_subject(alert_data):
    return f"🚨 {alert_data['alert_type'].upper()} Emergency Alert 🚨: Urgent Response needed at {alert_data['landmark']}, Reported at {now()}"

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
 
 
def send_email_message(all_data):
    number = "09982373882"
    
    if all_data['alert_type'] == 'police':
        custom = 'This is an emergency alert. Police assistance is urgently needed at the following location:'
    elif all_data['alert_type'] == 'health':
        custom = 'This is an emergency alert. An ambulance is urgently needed at the following location:'
    elif all_data['alert_type'] == 'fire':
        custom = 'This is an emergency alert. Fire response is urgently needed at the following location:'
    
    body = f"""
    <html>
        <body>
            <p><strong>To {all_data['name']},</strong></p>
            
            <h3><strong><p>{custom}</p></strong><h3>
            
            <h3><strong>📍 Location:</strong> {all_data['address']}<br>
            <strong>🕛 Date & Time:</strong> {now()}<br>
            <strong>👤 First Name: {all_data['user']['first_name']}</strong><br>
            <strong>👤 Last Name: {all_data['user']['last_name']}</strong><br>
            <strong>📞 Contact number: {all_data['contact_number']}</strong>
            </h3>
            
            <h3><a href="https://www.google.com/maps/place/{all_data['latitude']},{all_data['longitude']}">🗺️ Google Maps Link</a></h3>
            
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