from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from ..helpers import *
import sendgrid
from sendgrid.helpers.mail import Mail

class TwilioService():
    def __init__(self):
        self.sms = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        
    def send_sms(self, message, receiver, sender = settings.TWILIO_PHONE_NO):
        try:
            self.sms.messages.create(
            from_=sender,
            to=receiver,
            body=message
            )
            print("success")
            return True
        except TwilioRestException as t:
            print(t.code, t.msg)
            return False
        except Exception as e:
            print(e)
            return False
        