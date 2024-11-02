from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Alert, Resident

class AlertSerializer(serializers.ModelSerializer):
    
    ALERT_TYPE = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )
    
    resident = serializers.UUIDField()
    
    admin = serializers.UUIDField(required=False)
    
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
    