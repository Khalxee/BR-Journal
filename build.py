#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docuapp.settings')
    django.setup()
    
    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    print("✅ Static files collected successfully!")