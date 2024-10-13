from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.alert_serializer import AlertSerializer, SMSSerializer
from ..messages import *
from ..helpers import response, send_medical_response, send_fire_response, send_police_response, default_response, convert_to_639
from ..models import Alert
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..services.twilio import TwilioService
from django.conf import settings


class CreateAlertView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response(serializer.data, SUCCESS, status.HTTP_201_CREATED)
    
    
class SendSmsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        route = request.path.split("/")[-1]
        
        serializer = SMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            receiver = serializer.validated_data['receiver']
            location = serializer.validated_data['location']
            convert = convert_to_639(receiver)
            
            if route == 'fire':
                message = send_fire_response(location)
            elif route == 'medical':
                message = send_medical_response(location)
            elif route == 'police':
                message = send_police_response(location)
            else:
                message = default_response(location)
            
            twilio = TwilioService()
            twilio.send_sms(message, receiver=convert)
            return response(True, SUCCESS, status.HTTP_200_OK)
        except Exception as e:
            return response(False, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        
        