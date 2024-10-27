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
            sms = self.client.messages.create(
            from_=sender,
            to=receiver,
            body=message
            )
            print(sms)
            return True
        except TwilioRestException as t:
            print(t.code, t.msg)
            return False
        except Exception as e:
            return False
        