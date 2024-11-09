from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from ..serializers.department_serializer import DepartmentSerializer
from ..messages import *
from ..helpers import response
from ..models import Department
from ..data import departments_data
from ..permissions import IsAdmin


class GetDepartmentsView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        departments = Department.objects.all().order_by('-created_at', '-updated_at')
        serializer = DepartmentSerializer(departments, many=True)
        return response(serializer.data, SUCCESS, status.HTTP_200_OK)
    
class GenerateDepartmentsView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        departments = []

        for data in departments_data:
            departments.append(
                Department(
                name=data['name'],
                email=data['email'],
                tags=data['tags'],
                contact_number=data['contact_number'],
                address=data['address']
            )
            )

        try:
            Department.objects.bulk_create(departments)
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
        return response(True, SUCCESS, status.HTTP_201_CREATED)
    
class GetAvailableCountView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        
        fire = Department.objects.filter(tags="fire", status="available").count()
        health = Department.objects.filter(tags="health", status="available").count()
        police = Department.objects.filter(tags="police", status="available").count()
        
        return response({
            "fire": fire,
            "health": health,
            "police": police
        }, SUCCESS, status.HTTP_200_OK)
        
        
class CreateDepartmentView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                serializer.save()
                return response(serializer.data, SUCCESS, status.HTTP_201_CREATED)
            return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return response(False, EXISTS, status.HTTP_400_BAD_REQUEST)
        
    
class SetToAvailable(APIView):
    permission_classes = [IsAdmin]
    
    def patch(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        print(serializer.data['status'])
        
        if serializer.data['status'] == 'available':
            return response(False, 'The department is already set to available.', status.HTTP_400_BAD_REQUEST)
        
        department.status = 'available'
        department.save()
        
        return response(True, SUCCESS, status.HTTP_200_OK)
    

class UpdateDepartmentView(APIView):
    permission_classes = [IsAdmin]
    def put(self, request, pk):
        try:
            resident = Department.objects.get(pk=pk)
            serializer = Department(resident, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return response(True, UPDATED, status.HTTP_200_OK)
            return response(serializer.errors, BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
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
    permission_classes = [IsAdmin]
    def delete(self, request, pk):
        try:
            resident = Department.objects.get(pk=pk)
            resident.delete()
            return response(True, DELETED, status.HTTP_200_OK)
        except Department.DoesNotExist:
            return response(False, NOT_FOUND, status.HTTP_404_NOT_FOUND)
