from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.admin_serializer import AdminSerializer, LoginSerializer
from ..messages import *
from ..helpers import response, format_response
from django.conf import settings
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
    
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        admin = serializer.validated_data['admin']

        token, created = Token.objects.get_or_create(user=user)

        admin_serializer = AdminSerializer(admin)
        
        return response({
            "user": admin_serializer.data, 
            "token": token.key
            }, 
            SUCCESS, 
            status.HTTP_200_OK)
        
        
        
class AdminRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        serializer = AdminSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                serializer.save()
                return response(serializer.data, CREATED, status.HTTP_201_CREATED)
        except IntegrityError as e:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        
        return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        
        
    
    