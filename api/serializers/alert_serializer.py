from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Alert

class AlertSerializer(serializers.ModelSerializer):
     

    message = serializers.CharField(
        validators=[letters_only],
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Message is required.'
        }
    )
    
    class Meta:
        model = Alert
        fields = '__all__'
 
