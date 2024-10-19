from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.user_serializer import ResidentSerializer, UserSerializer
from ..messages import *
from ..helpers import response
from ..models import Resident, User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class GetResidentsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = Resident.objects.all()
        serializer = ResidentSerializer(data, many=True)
        return response(serializer.data, SUCCESS, status.HTTP_200_OK)

class PaginateResidentsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        paginator = LimitOffsetPagination()
        data = Resident.objects.all()
        paginate_data = paginator.paginate_queryset(data, request)
        serializer = ResidentSerializer(paginate_data, many=True)
        return paginator.get_paginated_response(serializer.data)

class FindResidentView(APIView):
    permission_classes = [AllowAny]
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
                "email": data['email'],
                "username":data['username'],
                "user_type":  data['username'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at'],
                "contact_number":resident_data['contact_number'],
                "address":resident_data['address'],
                "landmark":resident_data['landmark'],
                "latitude":resident_data['latitude'],
                "longitude":resident_data['longitude'],
        }
        
        return response(response_data, SUCCESS, status.HTTP_200_OK)    
    
class CreateResidentView(APIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    def delete(self, request, pk):
        try:
            resident = Resident.objects.get(user_id=pk)
            resident.delete()
            return response(True, DELETED, status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)

class UpdateResidentView(APIView):
    permission_classes = [AllowAny]
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
