#!/usr/bin/env python3
"""
DocuApp Admin Setup Script
Creates admin account and configures user management system
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False
    return True

def main():
    print("="*60)
    print("🚀 DocuApp Admin System Setup")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the DocuApp root directory.")
        sys.exit(1)
    
    print("\n📋 Setting up DocuApp admin system...")
    
    # Step 1: Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    # Step 2: Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Warning: Static files collection failed, but continuing...")
    
    # Step 3: Create admin account
    print("\n👑 Creating DocuApp administrator account...")
    print("Follow the prompts to create your admin account:")
    
    try:
        subprocess.run([sys.executable, "manage.py", "create_admin"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to create admin account")
        return False
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        return False
    
    # Step 4: Create sample data (optional)
    print("\n📝 Would you like to create sample data? (y/N): ", end="")
    create_sample = input().strip().lower()
    
    if create_sample in ['y', 'yes']:
        if Path('create_sample_data.py').exists():
            if not run_command("python create_sample_data.py", "Creating sample data"):
                print("⚠️  Warning: Sample data creation failed, but continuing...")
    
    # Step 5: Setup complete
    print("\n" + "="*60)
    print("🎉 DocuApp Admin Setup Complete!")
    print("="*60)
    
    print("\n📊 What's been set up:")
    print("  ✅ Database migrations applied")
    print("  ✅ Administrator account created")
    print("  ✅ User management system configured")
    print("  ✅ Admin templates installed")
    print("  ✅ Admin views and URLs configured")
    
    print("\n🔗 Available URLs:")
    print("  • Main Dashboard: /dashboard/")
    print("  • User Management: /admin/users/")
    print("  • Create User: /admin/users/create/")
    print("  • Create Admin: /admin/users/create-admin/")
    print("  • Django Admin: /admin/")
    
    print("\n🚀 Next Steps:")
    print("  1. Start the development server: python manage.py runserver")
    print("  2. Visit http://localhost:8000 to access DocuApp")
    print("  3. Log in with your admin credentials")
    print("  4. Go to /admin/users/ to manage users")
    
    print("\n📚 Admin Features:")
    print("  • Full user management (create, edit, delete)")
    print("  • Role-based permissions (user, admin, superuser)")
    print("  • User status management (active/inactive)")
    print("  • Password reset functionality")
    print("  • User details and activity tracking")
    print("  • Search and filter capabilities")
    
    print("\n🔐 Security Notes:")
    print("  • Admin accounts have full system access")
    print("  • Regular users can only access their own data")
    print("  • Always use strong passwords for admin accounts")
    print("  • Monitor user activity through the admin dashboard")
    
    print("\n✨ Enjoy your DocuApp admin system!")

if __name__ == "__main__":
    main()
