import uuid 
from django.db import models
from django.core.validators import EmailValidator
class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                                                
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id, self.email



