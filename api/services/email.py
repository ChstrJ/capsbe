from django.conf import settings
from django.core.mail import send_mail
from ..helpers import *

class EmailService():
    
    def send_email(self, subject, message, to_email, from_email = settings.EMAIL_HOST_USER):
        try:
            email = send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                html_message=message,
                recipient_list=[to_email]
            )
            print(email)
            return True
        except Exception as e:
            print(e)
            return str(e)
