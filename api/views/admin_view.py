from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..models.admin import Resident
from ..serializers.admin_serializer import AdminSerializer
from ..constants import *
from ..helpers import format_response, response
from django.conf import settings
from twilio.rest import Client

@api_view(['POST'])
def send_sms(self, request):
    to_phone_number = request.data.get('phone_number')
    
    message_body = request.data.get('body')
    
    