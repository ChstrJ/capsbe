from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.department_serializer import DepartmentSerializer
from ..messages import *
from ..helpers import response
from ..models import Department
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import IntegrityError


class GetDepartmentsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        
        departments = Department.objects.all()
        
        serializer = DepartmentSerializer(departments, many=True)
        
        return response(serializer.data, SUCCESS, status.HTTP_200_OK)
    
class GenerateDepartmentsView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        departments_data = [
        {'name': 'Fire Department', 'email': 'fire@example.com', 'contact_number': '123-456-7890', 'address': '123 Fire St.'},
        {'name': 'Medical Department', 'email': 'medical@example.com', 'contact_number': '987-654-3210', 'address': '456 Medical Rd.'},
        {'name': 'Police Department','email': 'police@example.com', 'contact_number': '555-555-5555', 'address': '789 Police Ave.'},
        ]
        
        departments = [
            Department(
                name=data['name'],
                email=data['email'],
                contact_number=data['contact_number'],
                address=data['address']
            )
            for data in departments_data
        ]

        try:
            Department.objects.bulk_create(departments)
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response(True, SUCCESS, status.HTTP_201_CREATED)
        
        
class CreateDepartmentView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response(serializer.data, SUCCESS, status.HTTP_201_CREATED)
    

class UpdateDepartmentView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, pk):
        try:
            resident = Department.objects.get(pk=pk)
            serializer = Department(resident, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return response(True, UPDATED, status.HTTP_200_OK)
        except Department.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        try:
            resident = Department.objects.get(pk=pk)
            serializer = DepartmentSerializer(resident, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response(True, UPDATED, status.HTTP_200_OK)
            return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
            
    
class DeleteDepartmentView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, pk):
        try:
            resident = Department.objects.get(pk=pk)
            resident.delete()
            return response(True, DELETED, status.HTTP_200_OK)
        except Department.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
