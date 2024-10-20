from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from ..permissions import IsAdmin
from ..serializers.alert_serializer import AlertSerializer, SMSSerializer
from ..messages import *
from ..helpers import response, send_medical_response, send_fire_response, send_police_response, default_response, convert_to_639
from ..models import Alert, User, Resident
from ..services.twilio import TwilioService
from ..services.mailtrap import MailtrapService

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
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user = request.user
        
        resident = user.residents
        
        alert_data = {
            **request.data,
            'resident_id': resident.id
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
            route = request.data.get("alert_type")
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
    
class SendEmailView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        
        mailtrap = MailtrapService()
        
        email = mailtrap.send_email("test", "cheschesj@gmail.com")
        return response(email)
        