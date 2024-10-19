from django.contrib import admin
from .models import Resident, Admin, User
# Register your models here.

admin.site.register(Resident)
admin.site.register(Admin)
admin.site.register(User)
