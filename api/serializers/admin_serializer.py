from rest_framework import serializers 
from django.contrib.auth.hashers import make_password 
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import User

class AdminSerializer(serializers.ModelSerializer):
    
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
    
    email = serializers.EmailField(
        required=True,
        error_messages={
            'blank': 'Email is required.'
        }
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20,
        min_length=8,
        error_messages={
            'blank': 'Password is required.'
        }
     )

    class Meta:
        model = User
        fields = '__all__'


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
