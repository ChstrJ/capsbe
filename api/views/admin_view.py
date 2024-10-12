from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.admin_serializer import AdminSerializer
from ..messages import *
from ..helpers import response
from django.conf import settings
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

    
class AdminLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        email = request.data.get("email");
        password = request.data.get("password");
        
        if not email and not password:
            response("Error", LOGIN_REQUIRED, status.HTTP_400_BAD_REQUEST)
        
        credentials = authenticate(username=email, password=password)
        
        print(credentials)
        
        if credentials:
            
            serializer = AdminSerializer(credentials)
            
            token, created = Token.objects.get_or_create(credentials)
            return response(f"admin: {serializer.data} token: Bearer {token.key}")
        return response("Error", INVALID_CREDENTIALS, status.HTTP_400_BAD_REQUEST)
        
        
class AdminRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        serializer = AdminSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, CREATED, status.HTTP_201_CREATED)
        return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        
        
    
    