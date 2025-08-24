"""
Management command to create a DocuApp administrator account
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import getpass


class Command(BaseCommand):
    help = 'Create a DocuApp administrator account'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the admin account'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address for the admin account'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the admin account'
        )
        parser.add_argument(
            '--first-name',
            type=str,
            help='First name for the admin account'
        )
        parser.add_argument(
            '--last-name',
            type=str,
            help='Last name for the admin account'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Create a superuser instead of staff user'
        )

    def handle(self, *args, **options):
        self.stdout.write('='*50)
        self.stdout.write(self.style.SUCCESS('DocuApp Administrator Account Creation'))
        self.stdout.write('='*50)
        
        # Get username
        username = options['username']
        while not username:
            username = input('Enter username: ').strip()
            if not username:
                self.stdout.write(self.style.ERROR('Username cannot be empty'))
                continue
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(f'Username "{username}" already exists'))
                username = None
        
        # Get email
        email = options['email']
        while not email:
            email = input('Enter email address: ').strip()
            if not email:
                self.stdout.write(self.style.ERROR('Email cannot be empty'))
                continue
            try:
                validate_email(email)
            except ValidationError:
                self.stdout.write(self.style.ERROR('Invalid email format'))
                email = None
                continue
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(f'Email "{email}" already exists'))
                email = None
        
        # Get first name
        first_name = options['first_name']
        if not first_name:
            first_name = input('Enter first name: ').strip()
        
        # Get last name
        last_name = options['last_name']
        if not last_name:
            last_name = input('Enter last name: ').strip()
        
        # Get password
        password = options['password']
        while not password:
            password = getpass.getpass('Enter password: ')
            if not password:
                self.stdout.write(self.style.ERROR('Password cannot be empty'))
                continue
            if len(password) < 8:
                self.stdout.write(self.style.ERROR('Password must be at least 8 characters long'))
                password = None
                continue
            
            confirm_password = getpass.getpass('Confirm password: ')
            if password != confirm_password:
                self.stdout.write(self.style.ERROR('Passwords do not match'))
                password = None
        
        # Determine admin type
        is_superuser = options['superuser']
        if not is_superuser:
            admin_type = input('Create superuser? (y/N): ').strip().lower()
            is_superuser = admin_type in ['y', 'yes']
        
        # Create the user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=is_superuser,
                is_active=True
            )
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✅ Administrator account created successfully!'))
            self.stdout.write('')
            self.stdout.write('Account Details:')
            self.stdout.write(f'  Username: {username}')
            self.stdout.write(f'  Email: {email}')
            self.stdout.write(f'  Name: {first_name} {last_name}')
            self.stdout.write(f'  Type: {"Super Administrator" if is_superuser else "Administrator"}')
            self.stdout.write(f'  User ID: {user.id}')
            self.stdout.write('')
            self.stdout.write('🎉 You can now log in to DocuApp with these credentials!')
            self.stdout.write('📊 Access the admin panel at: /admin/users/')
            self.stdout.write('🔧 Access Django admin at: /admin/')
            self.stdout.write('')
            
        except Exception as e:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR(f'❌ Error creating admin account: {str(e)}'))
            self.stdout.write('')
