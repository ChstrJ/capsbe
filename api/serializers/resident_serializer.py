
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Resident


class ResidentSerializer(serializers.ModelSerializer):
    

    first_name = serializers.CharField(
        validators=[letters_only],
        max_length=50,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'First name is required.'
        }
    )
    
    last_name = serializers.CharField(
        validators=[letters_only],
        max_length=50,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Last name is required.'
        }
    )
    contact_number = serializers.CharField(
        max_length=11,
        min_length=11,
        required=True,
        validators=[numbers_only, format_09],
        error_messages={
            'blank': 'Contact Number is required.'
        }
    )
    
    address = serializers.CharField(
        max_length=50,
        min_length=3,
        validators=[letters_only],
        required=True,
        error_messages={
            'blank': 'Address is required.'
        }
    )

    landmark = serializers.CharField(
        required=True,
        max_length=50,
        min_length=3,
        validators=[letters_only],
        error_messages={
            'blank': 'Landmark is required.'
        }
    )
    
    email = serializers.EmailField(
        required=True,
        error_messages={
            'blank': 'Email is required.'
        }
    )
    
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            'blank': 'Password is required.'
        }
    )
    
    
    class Meta:
        model = Resident
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
        