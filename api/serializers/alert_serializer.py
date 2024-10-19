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
    
    alert_type = serializers.CharField(
        choices=ALERT_TYPE,
        validators=[letters_only],
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Message is required.',
            'invalid_choice': 'Invalid alert type. Choose one of: health, fire, police',
        }
    )
    
    class Meta:
        model = Alert
        fields = '__all__'
 

class SMSSerializer(serializers.Serializer):
    
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
 
 
 