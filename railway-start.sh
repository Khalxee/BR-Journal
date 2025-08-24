#!/bin/bash
echo "🚂 Starting BR Journal on Railway..."

# Run database migrations
python manage.py migrate

# Create sample data if database is empty (first deploy)
python manage.py shell -c "
from django.contrib.auth.models import User
from apps.journal.models import Department
if not User.objects.exists():
    print('Creating sample data for first deploy...')
    exec(open('manage.py').read())
    import django; django.setup()
    from django.core.management import call_command
    call_command('create_sample_data')
    print('✅ Sample data created successfully!')
else:
    print('✅ Database already has data, skipping sample creation')
"

# Collect static files
python manage.py collectstatic --noinput

# Start the server
python manage.py runserver 0.0.0.0:$PORT