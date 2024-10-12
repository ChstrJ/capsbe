
from rest_framework import serializers
from ..models.resident import Resident
from django.contrib.auth.hashers import make_password
from .validator import must_contains_letters, letters_only, numbers_only, format_09


class ResidentSerializer(serializers.ModelSerializer):
    
    full_name = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Full name is required.'
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
        required=True,
        error_messages={
            'blank': 'Address is required.'
        }
    )

    landmark = serializers.CharField(
        required=True,
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
        