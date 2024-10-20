from django.conf import settings
from django.core.mail import send_mail
from ..helpers import *

class MailtrapService():
    
    def send_email(subject, message, to_email, from_email = settings.DEFAULT_EMAIL):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email="hello@demomailtrap.com",
                recipient_list=[to_email]
            )
            return True
        except Exception as e:
            print(e)
            return str(e)
