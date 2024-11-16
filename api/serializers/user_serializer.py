from rest_framework import serializers 
from django.contrib.auth.hashers import make_password 
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Admin, User, Resident
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(
        max_length=50,
        validators=[letters_only],
        error_messages={
            'max_length': 'Maximum of 50 characters.'
        }
    )
    
    last_name = serializers.CharField(
        max_length=50,
        validators=[letters_only],
        error_messages={
            'max_length': 'Maximum of 50 characters.',
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
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        return user
    
    class Meta:
        model = User
        exclude = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', "username")
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AdminSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'admin'
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        admin = Admin.objects.create(user=user, **validated_data)
        return admin
    
    class Meta: 
        model = Admin
        fields = ["user"]
        
class ResidentSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    
    contact_number = serializers.CharField(
        max_length=11,
        min_length=11,
        required=True,
        validators=[numbers_only, format_09],
        error_messages={
            'blank': 'Contact Number is required.',
            'min_length': 'Minimum of 11 characters',
            'max_length': 'Maximum of 11 characters',
        }
    )
    
    address = serializers.CharField(
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Address is required.',
            'min_length': 'Minimum of 3 characters',
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
    
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'resident'
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        if not validated_data['verified']:
            validated_data['verified'] = False
            
        resident = Resident.objects.create(user=user, **validated_data)
        
        return resident
    
    class Meta:
        model = Resident
        fields = ["id", "user", "verified", "contact_number", "address", "landmark"]
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True) 
    password = serializers.CharField(required=True, write_only=True)
 
 
class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True) 
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        new_pass = data.get('new_password')
        conf_pass = data.get('confirm_password')
        
        if new_pass != conf_pass:
            raise serializers.ValidationError({
                'confirm_password': 'This field do not match with new_password'
                })
        
        return data
        
