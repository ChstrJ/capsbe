from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..models.resident import Resident
from ..serializers.resident_serializer import ResidentSerializer
from ..constants import *
from ..helpers import format_response

@api_view(['GET'])
def get_residents(request):
    data = Resident.objects.all()
    serializer = ResidentSerializer(data, many=True)
    
    return Response(format_response(serializer.data, SUCCESS), status=status.HTTP_200_OK)

@api_view(['GET'])
def paginate_residents(request):
    
    paginator = LimitOffsetPagination()
    
    data = Resident.objects.all()
    paginate_data = paginator.paginate_queryset(data, request)
    
    serializer = ResidentSerializer(paginate_data, many=True)
    
    return paginator.get_paginated_response(serializer.data)
    
@api_view(['GET'])
def find_resident(request, pk):
    try:
        resident = Resident.objects.get(pk=pk)
        
        serializer = ResidentSerializer(resident)
        
        return Response(format_response(serializer.data, SUCCESS), status=status.HTTP_200_OK)
    except Resident.DoesNotExist:
        return Response(format_response('This ID does not exists.', NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_resident(request):
    
    serializer = ResidentSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(format_response(serializer.data, SUCCESS), status=status.HTTP_201_CREATED) 
        except Exception as e:
            return Response(format_response({"message": str(e)}, ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(format_response(serializer.errors, ERROR), status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_resident(request, pk):
    
    try:
        resident = Resident.objects.get(pk=pk)
        
        resident.delete()
        
        return Response(format_response(True, SUCCESS), status=status.HTTP_200_OK)
        
    except Resident.DoesNotExist:
        return Response(format_response("This ID does not exists.", NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
def update_resident(request, pk):
    
    if request.method == 'PUT':
        try:
            resident = Resident.objects.get(pk=pk)
        
            serializer = ResidentSerializer(resident, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(format_response(True, SUCCESS), status=status.HTTP_200_OK)
            return Response(format_response(serializer.errors, ERROR), status=status.HTTP_400_BAD_REQUEST)
        
        except Resident.DoesNotExist:
            return Response(format_response("This ID does not exists.", NOT_FOUND), status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'PATCH':
        try:
            resident = Resident.objects.get(pk=pk)
        
            serializer = ResidentSerializer(resident, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(format_response(True, SUCCESS), status=status.HTTP_200_OK)
            return Response(format_response(serializer.errors, ERROR), status=status.HTTP_400_BAD_REQUEST)
        
        except Resident.DoesNotExist:
            return Response(format_response("This ID does not exists.", NOT_FOUND), status=status.HTTP_404_NOT_FOUND)