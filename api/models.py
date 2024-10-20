import uuid 
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    USER_TYPE = (
    ('admin', 'Admin'),
    ('resident', 'Resident'),
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                                                
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.user_type}"

class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admins")
    created_at = models.DateTimeField(auto_now_add=True)                                                
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Resident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="residents")
    address = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    verified = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ID: {self.id}"

class Alert(models.Model):
    
    ALERT_TYPE = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resident_id = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True, related_name="resident")
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, related_name="admin")
    alert_type = models.CharField(max_length=100, choices=ALERT_TYPE, null=True)
    message = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                                                   
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id

class Department(models.Model):

    TAGS = (
    ('fire', 'Fire'),
    ('health', 'Health'),
    ('police', 'Police')
    )

    STATUS = (
    ('dispatched', 'Dispatched'),
    ('available', 'Available'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, validators=[EmailValidator()], unique=True)
    contact_number = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True, default="available")
    tags = models.CharField(max_length=100, choices=TAGS, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id 

    

