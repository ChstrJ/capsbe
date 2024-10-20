from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Alert

class AlertSerializer(serializers.ModelSerializer):
    
    ALERT_TYPE = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )

    message = serializers.CharField(
        validators=[letters_only],
        max_length=100,
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
    
    receiver = serializers.CharField(
        validators=[numbers_only],
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'receiver number is required.'
        }
    )
    
    location = serializers.CharField(
        validators=[letters_only],
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Location is required.'
        }
    )
    