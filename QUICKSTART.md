# 🚀 BR Journal - Quick Start Guide

## What is BR Journal?

BR Journal is a team weekly update management system that enables team members to document their weekly progress across multiple categories with detailed status tracking.

## ⚡ Quick Setup (5 minutes)

### 1. Navigate to Project
```bash
cd "/Users/beverlybabida/Desktop/bbc projects/BR Journal"
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate  # Already created
```

### 3. Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python manage.py migrate
```

### 5. Create Sample Data
```bash
python manage.py shell
>>> from apps.journal.models import Department
>>> from django.contrib.auth.models import User
>>> 
>>> # Create departments
>>> Department.objects.get_or_create(name="Engineering", defaults={"description": "Software Development Team"})
>>> Department.objects.get_or_create(name="Marketing", defaults={"description": "Marketing and Communications"})
>>> Department.objects.get_or_create(name="Sales", defaults={"description": "Sales Team"}) 
>>> Department.objects.get_or_create(name="HR", defaults={"description": "Human Resources"})
>>> 
>>> # Create admin user (if needed)
>>> User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
>>> 
>>> exit()
```

### 6. Run Server
```bash
python manage.py runserver
```

### 7. Access Application
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🧪 Test the System

### Login Credentials
- **Admin**: admin / admin123
- **Or create new user**: http://127.0.0.1:8000/admin/

### Quick Test Flow
1. **Login** with admin credentials
2. **Go to Admin** → Create a regular user account
3. **Login as user** → Create your first journal entry
4. **Select department**, set date range, add highlights/challenges
5. **Save and view** your entry in the dashboard

## 📋 Key Features to Test

### ✅ **Dynamic Journal Creation**
- Add multiple highlights, challenges, strategies
- Set status for each item (Completed, In Progress, etc.)
- Use Ctrl/Cmd + Enter to add new items quickly

### ✅ **Dashboard Overview**
- View your entries and team updates
- Filter by department, date range
- Search across all content

### ✅ **Status Tracking**
- 🟢 Completed
- 🔵 In Progress  
- 🟡 On Hold
- ⚪ Not Started
- 🔴 Cancelled

### ✅ **Comments & Collaboration**
- Add comments to any journal entry
- Real-time AJAX comment addition
- Team collaboration features

## 🔧 Common Commands

```bash
# Reset database
python manage.py flush
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run in development
python manage.py runserver

# Access Django shell
python manage.py shell
```

## 📊 What You Can Do

### **Team Members:**
- ✅ Create weekly journal entries
- ✅ Edit own entries
- ✅ View all team entries
- ✅ Comment on entries
- ✅ Filter and search content

### **Administrators:**
- ✅ All team member features
- ✅ Manage users and departments
- ✅ Access all entries
- ✅ System administration

## 🎯 Next Steps

1. **Create Users**: Add your team members via admin panel
2. **Setup Departments**: Configure your organization structure  
3. **Create Entries**: Start documenting weekly updates
4. **Explore Features**: Try filtering, commenting, status tracking
5. **Customize**: Modify templates and styling as needed

## 📚 Additional Resources

- **Full Documentation**: `PRODUCT_KNOWLEDGE.md`
- **Setup Instructions**: `README.md`
- **Project Structure**: See `/apps/journal/` for main code
- **Templates**: `/templates/journal/` for UI customization

---

**🚀 You're ready to start using BR Journal!**

The system is fully functional with a SQLite database and ready for your team's weekly updates.