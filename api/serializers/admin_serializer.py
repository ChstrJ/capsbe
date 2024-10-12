from rest_framework import serializers 
from django.contrib.auth.hashers import make_password 
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Admin
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

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
        model = Admin
        exclude = ('last_login', 'is_superuser', 'is_staff', 'date_joined', 'created_at', 'updated_at', 'groups', 'user_permissions')
        


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)
        
        try:
            admin = Admin.objects.get(username=username)
        except Admin.DoesNotExist:
            raise serializers.ValidationError("Admin with this username does not exist.")

        if not user:
            raise AuthenticationFailed("Invalid email or password.")
        
        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")
        
        attrs['user'] = user
        attrs['admin'] = admin
        return attrs