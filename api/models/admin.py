import uuid 
from django.db import models
from django.core.validators import EmailValidator
class Admin(models.Model):
    id = models.UUIDDield(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=100, null=True, validators=[EmailValidator()])
    password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                                                
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id, self.email



