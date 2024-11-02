from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..serializers.user_serializer import ResidentSerializer
from ..messages import *
from ..helpers import response
from ..models import Resident, User
from ..permissions import IsAdmin

class GetResidentsView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        data = Resident.objects.all().order_by('-created_at', '-updated_at')
        serializer = ResidentSerializer(data, many=True)
        
        response_data = []
        
        for resident_data in serializer.data:
            
            user_data = resident_data.get('user')
            
            formatted_data = {
                "id": user_data.get('id'),
                "first_name": user_data.get('first_name'),
                "last_name": user_data.get('last_name'),
                "email": user_data.get('email'),
                "user_type": user_data.get('user_type'),
                "contact_number": resident_data.get('contact_number'),
                "address": resident_data.get('address'),
                "landmark": resident_data.get('landmark'),
                "created_at": user_data.get('created_at'),
                "updated_at": user_data.get('updated_at'),
            }
            
            response_data.append(formatted_data)
        
        return response(response_data, SUCCESS, status.HTTP_200_OK)

class PaginateResidentsView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        paginator = LimitOffsetPagination()
        data = Resident.objects.all().order_by('created_at')
        paginate_data = paginator.paginate_queryset(data, request)
        serializer = ResidentSerializer(paginate_data, many=True)
        return paginator.get_paginated_response(serializer.data)

class FindResidentView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request, pk):
        try:
            resident = Resident.objects.get(user_id=pk)
        except Resident.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
        
        serializer = ResidentSerializer(resident)
        
        resident_data = serializer.data
        
        data = resident_data.get('user')
        
        response_data = {
                "id": data['id'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "verified": resident_data['verified'],
                "email": data['email'],
                "user_type": data['user_type'],
                "contact_number": resident_data['contact_number'],
                "address": resident_data['address'],
                "landmark": resident_data['landmark'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at'],
        }
        
        return response(response_data, SUCCESS, status.HTTP_200_OK)    
    
class CreateResidentView(APIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        serializer = ResidentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return response(serializer.data, CREATED, status.HTTP_201_CREATED)
            except Exception as e:
                return response(e, SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)

class DeleteResidentView(APIView):
    permission_classes = [IsAdmin]
    def delete(self, request, pk):
        try:
            resident = Resident.objects.get(user_id=pk)
            resident.delete()
            return response(True, DELETED, status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)

class UpdateResidentView(APIView):
    permission_classes = [IsAdmin]
    def put(self, request, pk):
        try:
            resident = Resident.objects.get(user_id=pk)
            serializer = ResidentSerializer(resident, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return response(True, UPDATED, status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            resident = Resident.objects.get(user_id=pk)
            serializer = ResidentSerializer(resident, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response(True, UPDATED, status.HTTP_200_OK)
            return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        except Resident.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)

class VerifyResidentView(APIView):
    permission_classes = [IsAdmin]
    
    def patch(self, request, pk):
        try:
            resident = Resident.objects.get(user_id=pk)
        except Resident.DoesNotExist:
            return response (False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
        
        serializer = ResidentSerializer(resident, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        resident.verified = True
        resident.save()
        
        return response("Verified", SUCCESS, status.HTTP_200_OK)
    