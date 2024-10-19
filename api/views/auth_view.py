from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.user_serializer import UserSerializer, ResidentSerializer, AdminSerializer, LoginSerializer
from ..messages import *
from ..helpers import response, format_response
from django.conf import settings
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from ..models import User
 
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
        
        return response({
            "user": user_details.data, 
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
                "username": request.data.get("username"),
            }
        }

        resident_data = {
            "contact_number": request.data.get("contact_number"),
            "address": request.data.get("address"),
            "landmark": request.data.get("landmark"),
            "latitude": request.data.get("latitude"),
            "longitude": request.data.get("longitude"),
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
                "username": resident.user.username,
                "user_type": resident.user.user_type,
                "created_at": resident.user.created_at.isoformat(),
                "updated_at": resident.user.updated_at.isoformat(),
                "contact_number": resident.contact_number,
                "address": resident.address,
                "landmark": resident.landmark,
                "latitude": resident.latitude,
                "longitude": resident.longitude,
                }
                
                return response(response_data, CREATED, status.HTTP_201_CREATED)
        except IntegrityError as e:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
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
                "username": request.data.get("username"),
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
                "username": admin.user.username,
                "user_type": admin.user.user_type,
                "created_at": admin.user.created_at.isoformat(),
                "updated_at": admin.user.updated_at.isoformat(),
                }
                
                return response(response_data, CREATED, status.HTTP_201_CREATED)
        except IntegrityError as e:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        
    
    