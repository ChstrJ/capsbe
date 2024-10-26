
from django.core.management import BaseCommand
from faker import Faker
from ...models import Resident, Alert, Department, Admin, User
from ...serializers.user_serializer import UserSerializer, ResidentSerializer

fake = Faker('en_PH')

class Command(BaseCommand):
    
    help = 'Create user account'
    
    def handle(self, *args, **kwargs):
        self.generate_account()
        self.create_resident()
        
    def generate_account(self):
        
        user = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@gmail.com",
            "password": "admin123"
        }
        
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        self.stdout.write("Admin account created!")
        
    def create_resident(self):
        
        user_data = {
            "user": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": 'test1@gmail.com',
                "password": '123123123',
            }
        }

        resident_data = {
            "contact_number": '09477936942',
            "address": fake.address(),
            "verified": True,
            "landmark": "Agora",
            "latitude": fake.latitude(),
            "longitude": fake.longitude(),
        }
        
        data = {**user_data, **resident_data}
        
        serializer = ResidentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.stdout.write("Resident account created!")