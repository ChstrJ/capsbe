from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from ..serializers.user_serializer import UserSerializer, ResidentSerializer, AdminSerializer, LoginSerializer
from ..messages import *
from ..helpers import response
from ..models import User, Resident
 
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response("User does not exists", NOT_FOUND, status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return response(False, INVALID_CREDENTIALS, status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        user_details = UserSerializer(user)
        
        data = user_details.data
        
        if user_details.data['user_type'] == 'resident':
            resident_id = user_details.data['id']
            resident = Resident.objects.get(user_id=resident_id)
            resident = ResidentSerializer(resident)
            
            resident_data = resident.data
            
            formatted_data = {
                "id": resident_data.get('id'),
                "first_name": data.get('first_name'),
                "last_name": data.get('last_name'),
                "email": data.get('email'),
                "user_type": data.get('user_type'),
                "verified": resident_data.get('verified'),
                "contact_number": resident_data.get('contact_number'),
                "address": resident_data.get('address'),
                "landmark": resident_data.get('landmark'),
                "created_at": data.get('created_at'),
                "updated_at": data.get('updated_at'),
            }
            
            data = formatted_data

            if not resident.data['verified']:
                return response("You are not verified. Please contact your barangay official to get verified.", PERMISSION_DENIED, status.HTTP_403_FORBIDDEN)
        
        return response({
            **data,
            "token": token.key
            }, 
            SUCCESS, 
            status.HTTP_200_OK)
        
class ResidentRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        user_data = {
            "user": {
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "email": request.data.get("email"),
                "password": request.data.get("password"),
            }
        }

        resident_data = {
            "contact_number": request.data.get("contact_number"),
            "address": request.data.get("address"),
            "verified": request.data.get("verified"),
            "landmark": request.data.get("landmark"),
        }
        
        data = {**user_data, **resident_data}
        
        serializer = ResidentSerializer(data=data)
        
        try:
            if serializer.is_valid():
                resident = serializer.save()
                
                response_data = {
                "id": str(resident.user.id),
                "first_name": resident.user.first_name,
                "last_name": resident.user.last_name,
                "email": resident.user.email,
                "verified": resident.verified,
                "user_type": resident.user.user_type,
                "created_at": resident.user.created_at.isoformat(),
                "updated_at": resident.user.updated_at.isoformat(),
                "contact_number": resident.contact_number,
                "address": resident.address,
                "landmark": resident.landmark,
                }
                
                return response(response_data, CREATED, status.HTTP_201_CREATED)
        except IntegrityError as e:
            return response(str(e), EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
                
class AdminRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        user_data = {
            "user": {
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "email": request.data.get("email"),
                "password": request.data.get("password"),
            }
        }
        
        serializer = AdminSerializer(data=user_data)
        
        try:
            if serializer.is_valid():
                admin = serializer.save()
                
                response_data = {
                "id": str(admin.user.id),
                "first_name": admin.user.first_name,
                "last_name": admin.user.last_name,
                "email": admin.user.email,
                "user_type": admin.user.user_type,
                "created_at": admin.user.created_at.isoformat(),
                "updated_at": admin.user.updated_at.isoformat(),
                }
                
                return response(response_data, CREATED, status.HTTP_201_CREATED)
        except IntegrityError as e:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
class GenerateAdminAccountView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        user = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@gmail.com",
            "password": "admin123"
        }
        
        serializer = UserSerializer(data=user)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response("Success!", SUCCESS, status.HTTP_200_OK)
