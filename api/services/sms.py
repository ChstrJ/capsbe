import requests
from django.conf import settings

class SMSService():
    
    def send_sms(self, number, message):
        url = f"https://sms.iprogtech.com/api/v1/sms_messages?api_token={settings.SMS_KEY}&phone_number={number}&message={message}"
        
        try:
            res = requests.post(url)
            print(res.json())
        except Exception as e:
            print(str(e))
            
        