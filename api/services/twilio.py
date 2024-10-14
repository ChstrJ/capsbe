from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from ..helpers import *
import sendgrid
from sendgrid.helpers.mail import Mail

class TwilioService():
    def __init__(self):
        self.sms = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        self.sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
        
    def send_sms(self, message, receiver, sender = settings.TWILIO_PHONE_NO):
        try:
            self.client.messages.create(
            from_=sender,
            to=receiver,
            body=message
            )
            return True
        except TwilioRestException as t:
            print(t.code, t.msg)
            return False
        except Exception as e:
            return False
        
    def send_email(self, to_email, subject, from_email = settings.DEFAULT_EMAIL):
        try:
            self.sg = Mail(
                from_email,
                to_email,
                subject,
                plain_text_content="test"
            )
            return True
        except TwilioRestException as t:
            print(t.code, t.msg)
            return False
        except Exception as e:
            print("error", e)
            return False
    

    