from rest_framework import serializers 
from ..models.admin import Admin              
from django.contrib.auth.hashers import make_password 
from .validator import must_contains_letters, letters_only, numbers_only, format_09

class AdminSerializer(serializers.ModelSerializer):

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
        model = Admin
        fields = '__all__'


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
