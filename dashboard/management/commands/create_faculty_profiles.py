from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Faculty, Department
import random

class Command(BaseCommand):
    help = 'Creates Faculty profiles for existing users with faculty usernames'

    def handle(self, *args, **options):
        # Get all users with faculty in their username who don't have Faculty profiles
        faculty_users = User.objects.filter(username__startswith='faculty')
        departments = Department.objects.all()
        
        if not departments.exists():
            self.stdout.write(self.style.ERROR('No departments found. Please create departments first.'))
            return
        
        created_count = 0
        for user in faculty_users:
            # Check if user already has a Faculty profile
            if not hasattr(user, 'faculty'):
                # Create a Faculty profile for the user
                department = random.choice(departments)
                employee_id = f"EMP{user.id:04d}"
                
                Faculty.objects.create(
                    user=user,
                    employee_id=employee_id,
                    department=department,
                    department_name=department.name,  # Add department_name field
                    designation="Assistant Professor",
                    phone=""
                )
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created Faculty profile for {user.username}'))
        
        if created_count == 0:
            self.stdout.write(self.style.WARNING('No new Faculty profiles created. All faculty users already have profiles.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} Faculty profiles'))