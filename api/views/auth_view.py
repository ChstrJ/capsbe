from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
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
    
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, SUCCESS, status.HTTP_200_OK)
        else:
            return response(serializer.errors, ERROR, status.HTTP_400_BAD_REQUEST)
        
class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        data = {current_password, new_password, confirm_password}
        
        if not current_password or not new_password or not confirm_password:
            return response({
                    'current_password': 'This field is required!',
                    'new_password': 'This field is required!',
                    'confirm_password': 'This field is required!'
                }, ERROR, status.HTTP_400_BAD_REQUEST)
        
        if not check_password(current_password, user.password):
            return response({
                'current_password': 'Your password does not match in our database.'
            }, ERROR, status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return response({
                'confirm_password': 'This field does not match with new_password.'
                }, ERROR, status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            user.password = make_password(new_password)
            user.save()
            return response(True, SUCCESS, status.HTTP_200_OK)
        
        return response(False, ERROR, status.HTTP_400_BAD_REQUEST)
        
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


class GetAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        
        serializer = UserSerializer(user)
        return response(serializer.data, SUCCESS, status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user.id
        
        try:
            user = User.objects.get(id=user_id)
            token = Token.objects.get(user=user)
            token.delete()
            return response(True, 'Succesfully logged out.', status.HTTP_200_OK)
        except Exception as e:
            return response(False, 'Token not found', status.HTTP_400_BAD_REQUEST)
        
