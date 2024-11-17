from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.conf import settings
from ..permissions import IsAdmin, IsResident
from ..serializers.user_serializer import ResidentSerializer, UserSerializer
from ..serializers.alert_serializer import AlertSerializer, SMSSerializer, UpdateAlertStatusSerializer
from ..serializers.department_serializer import DepartmentSerializer
from ..messages import *
from ..helpers import response, convert_to_639, send_sms_response, send_email_subject, send_email_message, respond_email_message, respond_sms_response, respond_email_subject
from ..models import Alert, Resident, Department, User
from ..services.twilio import TwilioService
from ..services.email import EmailService
from ..services.sms import SMSService

class CheckAlertActivityView(APIView):
    permission_classes = [IsResident]
    
    def get(self, request):
        user_id = request.user.residents
        
        alert = Alert.objects.filter(resident=user_id).first()

        serializer = AlertSerializer(alert)
        return Response({"alert_status": serializer.data['alert_status']})

class ListAlertsView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        status = request.GET.get('status')
        alert_type = request.GET.get('type')

        alerts = Alert.objects.all().order_by('-created_at', '-updated_at')

        if status:
            alerts = alerts.filter(alert_status=status)

        if alert_type:
            alerts = alerts.filter(alert_type=alert_type)


        serializer = AlertSerializer(alerts, many=True)
        
        data = []
        
        for alerts_data in serializer.data:
            
            alerts = alerts_data
            
            resident_data = Resident.objects.get(id=alerts['resident'])
            
            resident_data = ResidentSerializer(resident_data)
            resident_data = resident_data.data
            
            user_data = resident_data.get('user')
            
            formatted_data = {
                "id": alerts.get('id'),
                "resident": alerts.get('resident'),
                "admin": alerts.get('admin'),
                "alert_type": alerts.get('alert_type'),
                "alert_status": alerts.get('alert_status'),
                "message": alerts.get('message'),
                "latitude": alerts.get('latitude'),
                "longitude": alerts.get('longitude'),
                "first_name": user_data.get('first_name'),
                "last_name": user_data.get('last_name'),
                "address": resident_data.get('address'),
                "landmark": resident_data.get('landmark'),
                "created_at": alerts.get('created_at'),
                "updated_at": alerts.get('updated_at'),
            }
            
            data.append(formatted_data)
        
        return response(data, SUCCESS, 200)
        

class UpdateAlertStatusView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
            serializer = UpdateAlertStatusSerializer(alert, data=request.data)

            if serializer.is_valid():
                alert.alert_status = request.data.get('alert_status')
                alert.save()
                return response(True, SUCCESS, status.HTTP_200_OK)
            return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return response(False, ERROR, status.HTTP_400_BAD_REQUEST)
            
    
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
            'resident': resident.id,
        }
        
        serializer = AlertSerializer(data=alert_data)

        try:
            if serializer.is_valid():
                serializer.save()
                return response(serializer.data, SUCCESS, status.HTTP_201_CREATED)
            else:
                return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return response(False, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)

    
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
    
class SendDispatchView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        
        dept_id = request.data.get("department_id")
        alert_id = request.data.get("alert_id")
        
        if not dept_id or not alert_id:
            return response({
                'alert_id': 'This field is required.',
                'department_id': 'This field is required.'
                }, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
            
        try:
            #Alert Data 
            alert = Alert.objects.get(id=alert_id)

            if alert.alert_status == 'ongoing':
                return response("The emergency alert is already ongoing!", BAD_REQUEST, status.HTTP_400_BAD_REQUEST)

            alert.admin = request.user.admins
            alert.alert_status = 'ongoing'
            alert.save()

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
        except Exception as e:
            return response("Invalid Alert ID or Department ID", NOT_FOUND, status.HTTP_404_NOT_FOUND)
        
        # Combine all data
        user_data = {**user_data, **resident_data}
        dispatch_data = {**alert_data, **dept_data}
        
        email = EmailService()
        sms = SMSService()
        
        # Send to the department
        message_sms = send_sms_response(dispatch_data, user_data)
        subject = send_email_subject(dispatch_data, user_data)
        message_email = send_email_message(dispatch_data, user_data)
        
        # Send to the residents
        respond_sms = respond_sms_response(dispatch_data, user_data)
        respond_subject = respond_email_subject(dispatch_data, user_data)
        respond_message = respond_email_message(dispatch_data, user_data)
        
        if request.data.get("test_no"):
            department_no = request.data.get("test_no")
            resident_no = request.data.get("test_no")
        else:
            department_no = dispatch_data['contact_number']
            resident_no = user_data['contact_number']
            
        if request.data.get("test_email"):
            department_email = request.data.get("test_email")
            resident_email = request.data.get("test_email")
        else:
            department_email = dispatch_data['email']
            resident_email = user_data['user']['email']
            
        try: 
            email.send_email(subject, message_email, department_email)
            email.send_email(respond_subject, respond_message, resident_email)
            sms.send_sms(department_no, message_sms)
            sms.send_sms(resident_no, respond_sms)
            return response(True, SENT, status.HTTP_200_OK)
        except Exception as e:
            return response(str(e), BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        
