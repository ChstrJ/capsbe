from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.conf import settings
from ..permissions import IsAdmin, IsResident
from ..serializers.user_serializer import ResidentSerializer, UserSerializer
from ..serializers.alert_serializer import AlertSerializer, SMSSerializer
from ..serializers.department_serializer import DepartmentSerializer
from ..messages import *
from ..helpers import response, convert_to_639, now, send_sms_response, send_email_subject, send_email_message, respond_email_message, respond_sms_response, respond_email_subject
from ..models import Alert, User, Resident, Department
from ..services.twilio import TwilioService
from ..services.email import EmailService

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
        
        dept_id = request.data.get("department_id")
        alert_id = request.data.get("alert_id")
        
        if not dept_id and not alert_id:
            raise ValidationError({"error": "alert_id and department_id is required!"})
            
        
        #Alert Data 
        alert = Alert.objects.get(id=alert_id)
        alert_serializer = AlertSerializer(alert)
        alert_data = alert_serializer.data
        
        # Department Data
        dept = Department.objects.get(id=dept_id)
        dept_serializer = DepartmentSerializer(dept, data=request.data, partial=True)
        dept_serializer.is_valid(raise_exception=True)
        dept.status = 'dispatched'
        dept.save()
        dept_data = dept_serializer.data
        
        # Residents Data
        resident = Resident.objects.get(id=alert_data['resident'])
        resident_serializer = ResidentSerializer(resident)
        resident_data = resident_serializer.data
        user_data = resident_data.get('user')
        
        # Combine all data
        user_data = {**user_data, **resident_data}
        dispatch_data = {**alert_data, **dept_data}
        
        email = EmailService()
        twilio = TwilioService()
        
        # Send to the department
        message_sms = send_sms_response(dispatch_data, user_data)
        subject = send_email_subject(dispatch_data, user_data)
        message_email = send_email_message(dispatch_data, user_data)
        
        # Send to the residents
        respond_sms = respond_sms_response(dispatch_data, user_data)
        respond_subject = respond_email_subject(dispatch_data, user_data)
        respond_message = respond_email_message(dispatch_data, user_data)
        
        # The number should be verified in twilio dashboard
        department_no = '09477936940' #all_data['contact_number']
        department_no = convert_to_639(department_no)
        
        try: 
            email.send_email(subject, message_email, dispatch_data['email'])
            email.send_email(respond_subject, respond_message, user_data['user']['email'])
            #twilio.send_sms(message_sms, receiver=convert)
            #twilio.send_sms(respond_sms,)
            return response(True, SUCCESS, status.HTTP_200_OK)
        except Exception as e:
            return response(str(e), BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        