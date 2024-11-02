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

def respond_sms_response(dispatch_data, user_data):
    
    if dispatch_data['alert_type'] == 'fire':
        response = f"EMERGENCY ALERT: Fire truck incoming on {user_data['address']}. Clear the way immediately and stay alert.\n" 
    elif dispatch_data['alert_type'] == 'medical':
        response = f"EMERGENCY ALERT: Medical assistance is on the way to {user_data['address']}. Please clear the area and allow emergency personnel to pass. Stay safe!\n" 
    elif dispatch_data['alert_type'] == 'police':
        response = f"EMERGENCY ALERT: Police are responding to an incident at {user_data['address']}. Please stay indoors and avoid the area for your safety.\n"
    else:
        response = f"Emergeton is on the way to {user_data['address']}. Please stay calm!"
        
    return response

def send_sms_response(dispatch_data, user_data):
    
    link = f"https://www.google.com/maps/place/{dispatch_data['latitude']},{dispatch_data['longitude']}"
    
    if dispatch_data['alert_type'] == 'fire':
        response = f"EMERGENCY ALERT: Fire truck needed at {user_data['address']}. Please respond immediately!\n" 
        #response += f"Google Maps Link: {link}"
    elif dispatch_data['alert_type'] == 'medical':
        response = f"EMERGENCY ALERT: Medical assistance is needed at {user_data['address']}. Please respond immediately!\n" 
        #response += f"Google Maps Link: {link}"
    elif dispatch_data['alert_type'] == 'police':
        response = f"EMERGENCY ALERT: Police are needed at {user_data['address']}. Please respond immediately!\n"
        #response += f"Google Maps Link: {link}"
    else:
        response = f"Emergeton is on the way to {user_data['address']}. Please respond immediately!"
        response += f"Google Maps Link: {link}"
        
        
    return response

def send_email_subject(dispatch_data, user_data):
    return f"🚨 {dispatch_data['alert_type'].upper()} EMERGENCY ALERT 🚨: Urgent Response needed at {user_data['landmark']}, Reported at {now()}"

def respond_email_subject(dispatch_data, user_data):
    return f"🚨 {dispatch_data['alert_type'].upper()} EMERGENCY ALERT 🚨: Help is on the way! Please stay calm. Assistance is headed to your location near {user_data['landmark']}."
    
def send_email_message(dispatch_data, user_data):
    number = "09982373882"
    
    if dispatch_data['alert_type'] == 'police':
        custom = 'This is an emergency alert. Police assistance is urgently needed at the following location:'
    elif dispatch_data['alert_type'] == 'health':
        custom = 'This is an emergency alert. An ambulance is urgently needed at the following location:'
    elif dispatch_data['alert_type'] == 'fire':
        custom = 'This is an emergency alert. Fire response is urgently needed at the following location:'
    
    body = f"""
    <html>
        <body>
            <p><strong>To {dispatch_data['name']},</strong></p>
            
            <h3><strong><p>{custom}</p></strong><h3>
            
            <h3><strong>📍 Location:</strong> {user_data['address']}<br>
            <strong>🕛 Date & Time:</strong> {now()}<br>
            <strong>👤 First Name: {user_data['user']['first_name']}</strong><br>
            <strong>👤 Last Name: {user_data['user']['last_name']}</strong><br>
            <strong>📞 Contact number: {user_data['contact_number']}</strong>
            </h3>
            
            <h3><a href="https://www.google.com/maps/place/{dispatch_data['latitude']},{dispatch_data['longitude']}">🗺️ Google Maps Link</a></h3>
            
            <p>Immediate assistance is required. Please respond as soon as possible. For any further information or updates, contact us at <strong>{number}</strong>.</p>
            
            <p>Best regards,<br>
            Barangay Longos Official</p>
        </body>
    </html>
    """
    
    return body

def respond_email_message(dispatch_data, user_data):
    number = "09982373882"
    
    if dispatch_data['alert_type'] == 'police':
        custom = 'Please stay alert. Police is coming on your way.'
    elif dispatch_data['alert_type'] == 'health':
        custom = 'Please stay alert. Medical assistance is coming on your way.'
    elif dispatch_data['alert_type'] == 'fire':
        custom = 'Please stay alert. Fire truck is coming on your way.'
    
    body = f"""
    <html>
        <body>
        <p><strong>Dear {user_data['user']['first_name']} {user_data['user']['last_name']},</strong></p>
        
        <h3>{custom}</h3>
        
        <p>We kindly ask you to remain calm. Help is on the way to your location. For further information or updates, please don't hesitate to contact us at <strong>{number}</strong>.</p>
        
        <p>Warm regards,<br>
        Barangay Longos Official</p>
    </body>
    </html>
    """
    
    return body   

def convert_to_639(number):
    
    if number[0] == "+":
        return 
    
    return f"+639{number[2:]}"
