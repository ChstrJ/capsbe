from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from ..helpers import *

class TwilioService():
    def __init__(self):
        self.client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        
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