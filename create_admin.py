#!/usr/bin/env python
import os
import django

def create_admin_user():
    """Force create admin user"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docuapp.settings')
    django.setup()
    
    from django.contrib.auth.models import User
    
    # Delete existing admin if exists and recreate
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.delete()
        print("🗑️ Deleted existing admin user")
    except User.DoesNotExist:
        print("ℹ️ No existing admin user found")
    
    # Create new admin user
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@brjournal.com',
        password='admin123'
    )
    admin_user.first_name = 'System'
    admin_user.last_name = 'Administrator'
    admin_user.save()
    
    print(f"✅ Created admin user: {admin_user.username}")
    print(f"✅ Admin password: admin123")
    print(f"✅ Admin is superuser: {admin_user.is_superuser}")
    print(f"✅ Admin is staff: {admin_user.is_staff}")
    
    return admin_user

if __name__ == '__main__':
    create_admin_user()