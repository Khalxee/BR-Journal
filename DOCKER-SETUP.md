# 🐳 DocuApp Docker Setup Guide

This guide will help you set up and run DocuApp using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose available

## Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd "/users/beverlybabida/desktop/bbc projects/docuapp"
   ```

2. **Run the setup script:**
   ```bash
   chmod +x docker-setup.sh
   ./docker-setup.sh
   ```

3. **Create a superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application:**
   - Main app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin/

## Manual Setup (Alternative)

If you prefer to set up manually:

1. **Build the containers:**
   ```bash
   docker-compose build
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

3. **Run migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Collect static files:**
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

## Services Overview

The Docker setup includes these services:

- **web**: Django application (port 8000)
- **db**: PostgreSQL database
- **redis**: Redis cache and task queue
- **vite**: Frontend development server (port 5173)
- **celery**: Background task processor

## Accessing the Application

### 🌐 Main Application
- **URL**: http://localhost:8000
- **Login**: Use the superuser account you created
- **Features**: Full DocuApp functionality

### 👑 Admin Panel
- **URL**: http://localhost:8000/admin/
- **Login**: Superuser credentials
- **Features**: Django admin interface

### 🔧 Development Server
- **URL**: http://localhost:5173
- **Purpose**: Hot reloading for frontend assets
- **Note**: Only needed during development

## User Management

### Creating Users

1. **Via Admin Panel:**
   - Go to http://localhost:8000/admin/
   - Login with superuser credentials
   - Navigate to Users → Add user
   - Set email, password, and role

2. **Via Shell:**
   ```bash
   docker-compose exec web python manage.py shell
   ```
   ```python
   from apps.users.models import CustomUser
   user = CustomUser.objects.create_user(
       email='editor@example.com',
       password='password123',
       role='editor'
   )
   ```

### User Roles

- **Admin**: Full system access, user management
- **Editor**: Create and edit documents
- **Viewer**: Read-only access to published documents

## Useful Commands

### Container Management
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Restart specific service
docker-compose restart web

# Access container shell
docker-compose exec web bash
```

### Database Management
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Reset database (⚠️ This will delete all data)
docker-compose down
docker volume rm docuapp_postgres_data
docker-compose up -d
```

### Django Management
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Run Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Find what's using port 8000
   lsof -i :8000
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database connection errors:**
   ```bash
   # Check if database is running
   docker-compose ps
   # View database logs
   docker-compose logs db
   ```

3. **Migration errors:**
   ```bash
   # Reset migrations (⚠️ This will delete all data)
   docker-compose exec web python manage.py migrate --fake-initial
   ```

4. **Permission errors:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web

# Last 50 lines
docker-compose logs --tail=50 web
```

## Development Workflow

1. **Code changes**: Edit files normally - they're mounted as volumes
2. **Python changes**: Container automatically reloads Django
3. **Frontend changes**: Vite service provides hot reloading
4. **Database changes**: Run migrations after model changes

## File Structure

```
docuapp/
├── docker-compose.yml    # Docker services configuration
├── Dockerfile.dev        # Django app container
├── Dockerfile.vite       # Vite development container
├── .env                  # Environment variables
└── docker-setup.sh       # Quick setup script
```

## Next Steps

1. **Create users** with different roles
2. **Upload documents** to test functionality
3. **Test role-based access** by switching users
4. **Customize** the application as needed

## Production Deployment

For production deployment:
1. Update environment variables in `.env`
2. Set `DEBUG=False`
3. Configure proper database credentials
4. Set up proper static file serving
5. Use production-grade web server (nginx + gunicorn)

---

Need help? Check the main README.md or create an issue in the repository.
