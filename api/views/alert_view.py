from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from ..serializers.alert_serializer import AlertSerializer
from ..messages import *
from ..helpers import response
from ..models import Alert
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class CreateAlertView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = AlertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

