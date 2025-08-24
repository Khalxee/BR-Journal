# BR Journal - Team Weekly Updates Application

A Django-based web application for managing team weekly journal entries where team members can document their weekly highlights, challenges, strategies, and more.

## Features

### Core Functionality
- **Weekly Journal Entries**: Team members can create weekly reports with structured fields
- **Department Organization**: Entries are organized by departments
- **Comprehensive Reporting**: Each entry includes:
  - Date range (from/to)
  - Department
  - Highlights (achievements and successes)
  - Pendings (ongoing tasks)
  - Challenges (obstacles and issues)
  - Personal Updates (professional development)
  - Strategies (plans and next steps)

### User Experience
- **Dashboard**: Overview with statistics and recent entries
- **Filtering & Search**: Filter entries by department, date range, or search content
- **Comments System**: Team members can comment on entries
- **Responsive Design**: Works on desktop and mobile devices
- **User Authentication**: Secure login system with Django Allauth

### Technical Features
- Built with Django 4.2.7
- Bootstrap 5 responsive UI
- PostgreSQL database support
- Docker containerization ready
- Admin interface for management
- Comprehensive test coverage

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+ (optional, for frontend assets)
- PostgreSQL (or SQLite for development)

### Quick Start

1. **Navigate to project directory**:
   ```bash
   cd "/Users/beverlybabida/Desktop/bbc projects/BR Journal"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**:
   - Copy `.env.example` to `.env` (if available)
   - Update database settings and secret key in `.env`

5. **Database setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Create sample departments** (optional):
   ```bash
   python manage.py shell
   >>> from apps.journal.models import Department
   >>> Department.objects.create(name="Engineering", description="Software Development Team")
   >>> Department.objects.create(name="Marketing", description="Marketing and Communications")
   >>> Department.objects.create(name="Sales", description="Sales Team")
   >>> exit()
   ```

8. **Run development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   - Main app: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage Guide

### For Team Members

1. **Login**: Access the application and log in with your credentials
2. **Dashboard**: View your recent entries and team updates
3. **Create Entry**: Click "New Entry" to create a weekly journal
4. **Fill Details**:
   - Select your department
   - Set the date range (from/to)
   - Fill in your highlights, challenges, strategies, etc.
5. **View & Edit**: Access your entries to view or edit them
6. **Comments**: Add comments to team members' entries for collaboration

### For Administrators

1. **Admin Panel**: Access `/admin/` to manage:
   - Users and permissions
   - Departments
   - Journal entries
   - Comments

2. **User Management**: Create accounts for team members
3. **Department Setup**: Create and manage organization departments

## Project Structure

```
BR Journal/
├── apps/
│   ├── journal/          # Main journal application
│   │   ├── models.py     # Database models
│   │   ├── views.py      # View logic
│   │   ├── forms.py      # Form definitions
│   │   ├── urls.py       # URL routing
│   │   └── admin.py      # Admin configuration
│   ├── users/            # User management
│   ├── web/              # General web pages
│   └── documents/        # Document handling
├── templates/journal/    # HTML templates
├── docuapp/             # Django settings
└── requirements.txt     # Python dependencies
```

## API Endpoints

- `/` - Dashboard (main page)
- `/list/` - List all journal entries
- `/create/` - Create new journal entry
- `/detail/<id>/` - View journal entry details
- `/update/<id>/` - Edit journal entry
- `/comment/<id>/` - Add comment (AJAX)

## Docker Setup (Optional)

If Docker files are present, you can run with Docker:

```bash
docker-compose up --build
```

## Contributing

1. Create feature branches for new functionality
2. Write tests for new features
3. Follow Django coding standards
4. Update documentation as needed

## Support

For technical issues or feature requests, contact the development team or create issues in your project management system.

---

**Version**: 1.0.0  
**Last Updated**: August 2025
