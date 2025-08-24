#!/bin/bash
echo "Building BR Journal for Vercel..."

# Install dependencies
pip install -r requirements.txt

# Run Django setup commands
python manage.py collectstatic --noinput --clear
python manage.py migrate

# Create public directory with static files
mkdir -p public/static
cp -r static/* public/static/ 2>/dev/null || true

echo "Build completed successfully!"
