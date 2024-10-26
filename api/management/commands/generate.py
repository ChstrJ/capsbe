from django.core.management import BaseCommand
from models import Resident, Alert, Department, Admin
from faker import Faker

fake = Faker('en_PH')

class Command(BaseCommand):
    
    help = 'Generate dummy data'
    
    def handle(self, *args, **kwargs):
        
        count = kwargs['count']
        
        self.generate_account()
        self.generate_department(count=count)
        #self.generate_alerts(count=count)
        #self.generate_residents(count=count)
        
    def generate_account(self):
        
        
        pass
    
    def generate_department(self, count = 10):
        
        for _ in range(count):
            Department.objects.create(
                name=fake.department(),
                email=fake.name(),
                tags=fake.random_choices(['fire', 'health', 'police']),
                contact_number=fake.phone_number(),
                address=fake.address()
            )
            
            
        self.stdout.write('Department Done!')
        
    def generate_alerts(self, count = 10):
        
        self.stdout.write('Alerts Done!')
    
    def generate_residents(self, count = 10):
        
        self.stdout.write('Alerts Done!')