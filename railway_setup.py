#!/usr/bin/env python
import os
import django
import subprocess
import sys

def run_setup():
    """Ensure Django setup runs before server starts"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docuapp.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    print("🔧 FORCING database migrations...")
    
    # Run makemigrations first to ensure all migrations exist
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
    except:
        pass
    
    # Force migrate with fake-initial for existing tables
    try:
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    except Exception as e:
        print(f"Migration error: {e}")
        # Try without syncdb
        execute_from_command_line(['manage.py', 'migrate'])
    
    print("🏗️ Creating Django site...")
    try:
        from django.contrib.sites.models import Site
        site, created = Site.objects.get_or_create(id=1, defaults={'domain': 'br-journal.up.railway.app', 'name': 'BR Journal'})
        if created:
            print(f"✅ Created site: {site}")
        else:
            print(f"✅ Site exists: {site}")
    except Exception as e:
        print(f"Site creation error: {e}")
    
    # Check if we need sample data
    try:
        from django.contrib.auth.models import User
        if not User.objects.exists():
            print("📊 Creating sample data...")
            execute_from_command_line(['manage.py', 'create_sample_data'])
            print("✅ Sample data created!")
        else:
            print("✅ Database already has users")
    except Exception as e:
        print(f"Sample data error: {e}")
    
    print("🎨 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    except Exception as e:
        print(f"Static files error: {e}")
    
    print("🚀 Setup completed! Starting server...")

if __name__ == '__main__':
    run_setup()
    
    # Start the server
    port = os.environ.get('PORT', '8000')
    subprocess.run([sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}'])