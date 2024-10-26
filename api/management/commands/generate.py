from django.core.management import BaseCommand
from ...models import Resident, Alert, Department, Admin, User
from faker import Faker
from ...serializers.user_serializer import UserSerializer, ResidentSerializer
from ...serializers.alert_serializer import AlertSerializer
import random

fake = Faker('en_PH')

class Command(BaseCommand):
    
    help = 'Generate dummy data'
    
    def add_arguments(self, parser):
        
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake records you want to create.'
        )
    
    def handle(self, *args, **kwargs):
        
        count = kwargs['count']
        
        self.generate_department(count=count)
        self.generate_residents(count=count)
        self.generate_alerts(count=count)
        
    def generate_department(self, count = 10):
        
        for _ in range(count):
            Department.objects.create(
                name=fake.name(),
                email=fake.name(),
                tags=random.choice(['fire', 'health', 'police']),
                contact_number='09477936942',
                address=fake.address(),
                status=random.choice(['available', 'dispatched'])
            )
            
            
        self.stdout.write('Departments Done!')
        
        
    def generate_residents(self, count = 10):
        
        data = []
        for _ in range(count):
            
            user_data = {
            "user": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "password": "test123123",
            }
            }

            resident_data = {
            "contact_number": "09477936945",
            "address": fake.address(),
            "verified": random.choice([True, False]),
            "landmark": "Malabon"
            }
            
            temp = {**user_data, **resident_data}
            
            data.append(temp)
        
        serializer = ResidentSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        self.stdout.write('Residents Done!')
        
    def generate_alerts(self, count = 10):
        
        data = []
        
        residents_ids = Resident.objects.values_list('id', flat=True)
        
        for _ in range(count):
            
            residents_id = random.choice(residents_ids)
            
            alert_data = {
            'resident_id': residents_id,
            'message': "test test test",
            'alert_type': random.choice(['fire', 'health', 'police']),
            "latitude": random.choice(['14.6538']),
            "longitude": random.choice(['120.9602']),
            }
            
            data.append(alert_data)
            
        serializer = AlertSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        self.stdout.write('Alerts Done!')
    
    