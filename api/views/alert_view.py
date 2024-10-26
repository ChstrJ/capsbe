from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from ..permissions import IsAdmin, IsResident
from ..serializers.alert_serializer import AlertSerializer, SMSSerializer
from ..messages import *
from ..helpers import response, convert_to_639, now, send_sms_response, send_email_subject, send_email_message
from ..models import Alert, User, Resident
from ..services.twilio import TwilioService
from ..services.email import EmailService
import asyncio

class ListAlertsView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return response(serializer.data, SUCCESS, status.HTTP_200_OK)
    
class FindAlertView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
            serializer = AlertSerializer(alert)
            return response(serializer.data, SUCCESS, status.HTTP_200_OK)
        except Alert.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
        
class DeleteAlertView(APIView):
    permission_classes = [IsAdmin]
    def delete(self, request, pk):
        try:
            alerts = Alert.objects.get(pk=pk)
            alerts.delete()
            return response(True, SUCCESS, status.HTTP_200_OK)
        except Alert.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)

class CreateAlertView(APIView):
    permission_classes = [IsResident]
    def post(self, request):
        
        resident = request.user.residents
        
        alert_data = {
            **request.data,
            'resident_id': resident.id,
        }
        
        serializer = AlertSerializer(data=alert_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response(serializer.data, SUCCESS, status.HTTP_201_CREATED)
    
    
class SendSmsView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        
        serializer = SMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            type = serializer.validated_data['alert_type']
            receiver = serializer.validated_data['receiver']
            location = serializer.validated_data['address']
            convert = convert_to_639(receiver)
            
            message = send_sms_response(location, type)           
            twilio = TwilioService()
            twilio.send_sms(message, receiver=convert)
            return response(True, SUCCESS, status.HTTP_200_OK)
        except Exception as e:
            return response(False, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
    
class SendEmailView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        
        email = EmailService()
        
        subject = send_email_subject("navotas", "fire")
        message = send_email_message("address 123 123", "fire department", "fire", "0947793941")
        to_email = "cheschesj2@gmail.com"
        
        try: 
            email.send_email(subject, message, to_email)
            return response(True, SUCCESS, status.HTTP_200_OK)
        except Exception as e:
            return response(str(e), BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        