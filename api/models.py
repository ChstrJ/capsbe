import uuid 
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser

class Admin(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    email = models.CharField(max_length=100, null=True, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                                                
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Resident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ID: {self.id} Email: {self.email}"

class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resident_id = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="resident_alerts")
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name="admin_alerts")
    from_location = models.CharField(max_length=100, null=True)
    to_location = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                                                   
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id


   
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, validators=[EmailValidator()], unique=True)
    contact_number = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id 

    
