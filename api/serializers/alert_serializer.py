from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Alert, Resident, Admin

class AlertSerializer(serializers.ModelSerializer):
    
    ALERT_TYPE = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )

    ALERT_STATUS = (
    ('ongoing', 'Ongoing'),
    ('dismissed', 'Dismissed'),
    ('pending', 'Pending'),
    ('done', 'Done'),
    )

    
    resident = serializers.PrimaryKeyRelatedField(queryset=Resident.objects.all(), required=False)
    admin = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.all(), required=False)
    
    message = serializers.CharField(
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Message is required.'
        }
    )
    
    alert_type = serializers.ChoiceField(
        required=True,
        choices=ALERT_TYPE,
        error_messages={
            'blank': 'Alert type is required.',
            'invalid_choice': 'Please choose the following: police, health, fire'
        }
    )

    alert_status = serializers.ChoiceField(
        required=False,
        choices=ALERT_STATUS,
        error_messages={
            'invalid_choice': 'Please choose the following: ongoing, pending, dismissed, done'
        }
    )

    
    latitude = serializers.DecimalField(
        max_digits=12,
        decimal_places=8, 
        required=True, 
        error_messages={
            'blank': 'Latitude is required.'
        }
    )
    
    longitude = serializers.DecimalField(
        max_digits=12, 
        decimal_places=8, 
        required=True, 
        error_messages={
            'blank': 'Longitude is required.'
        }
    )
    
    class Meta:
        model = Alert
        fields = '__all__'

class UpdateAlertStatusSerializer(serializers.ModelSerializer):

    ALERT_STATUS = (
    ('ongoing', 'Ongoing'),
    ('dismissed', 'Dismissed'),
    ('pending', 'Pending'),
    ('done', 'Done'),
    )
    
    alert_status = serializers.ChoiceField(
        required=True,
        choices=ALERT_STATUS,
        error_messages={
            'invalid_choice': 'Please choose the following: ongoing, pending, dismissed, done'
        }
    )

    class Meta:
        model = Alert
        fields = '__all__'


class SMSSerializer(serializers.Serializer):
    
    ALERT_TYPE = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )

    
    alert_type = serializers.ChoiceField(
        required=True,
        choices=ALERT_TYPE,
        error_messages={
            'blank': 'Alert type is required.',
            'invalid_choice': 'Please choose the following: police, health, fire'
        }
    )
    
    address = serializers.CharField(
        validators=[letters_only],
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Address is required.'
        }
    )
    
