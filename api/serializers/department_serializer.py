
from rest_framework import serializers
from .validator import must_contains_letters, letters_only, numbers_only, format_09
from ..models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Name is required.'
        }
    )

    tags = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        error_messages={
            'blank': 'Tags is required.'
        }
    )


    
    email = serializers.EmailField(
        required=True,
        error_messages={
            'blank': 'Email is required.'
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
    
    
    class Meta:
        model = Department
        fields = '__all__'
        
