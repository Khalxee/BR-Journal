#!/usr/bin/env python
import os
import django
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docuapp.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    print("🔧 Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("🏗️ Setting up Django sites framework...")
    execute_from_command_line(['manage.py', 'migrate', 'sites'])
    
    # Check if we need sample data
    from django.contrib.auth.models import User
    if not User.objects.exists():
        print("📊 Creating sample data...")
        execute_from_command_line(['manage.py', 'create_sample_data'])
        print("✅ Sample data created!")
    else:
        print("✅ Database already has data")
    
    print("🎨 Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("🚀 Railway deployment setup completed!")