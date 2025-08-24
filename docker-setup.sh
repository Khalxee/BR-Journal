#!/bin/bash

# DocuApp Docker Setup Script
echo "🐳 Setting up DocuApp with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

# Build and start the containers
echo "🏗️  Building containers..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create static directory
echo "📁 Creating static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "✅ DocuApp is now running!"
echo ""
echo "🌐 Access the application at: http://localhost:8000"
echo "📊 Vite dev server at: http://localhost:5173"
echo ""
echo "📋 Next steps:"
echo "1. Create a superuser: docker-compose exec web python manage.py createsuperuser"
echo "2. Access the admin panel: http://localhost:8000/admin/"
echo "3. Start creating users and documents!"
echo ""
echo "🛠️  Useful commands:"
echo "• View logs: docker-compose logs -f"
echo "• Stop containers: docker-compose down"
echo "• Restart containers: docker-compose restart"
echo "• Shell access: docker-compose exec web bash"
