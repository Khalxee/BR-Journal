#!/bin/bash

# BR Journal Setup Script
echo "🚀 Setting up BR Journal Application..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cat > .env << EOL
SECRET_KEY=django-insecure-$(python3 -c "import secrets; print(secrets.token_hex(25))")
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EOL
fi

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👤 Do you want to create a superuser account? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Create sample data (optional)
echo "📝 Do you want to create sample data for testing? (y/n)"
read -r create_sample
if [ "$create_sample" = "y" ] || [ "$create_sample" = "Y" ]; then
    python manage.py create_sample_data
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌟 To start the development server:"
echo "   python manage.py runserver"
echo ""
echo "🔗 Access the application:"
echo "   Main app: http://127.0.0.1:8000/"
echo "   Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "📚 Check README.md for detailed usage instructions."
echo ""
