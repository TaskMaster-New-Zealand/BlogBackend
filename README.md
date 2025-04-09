# blogBackend

A complete blog backend developed with Django and Django REST Framework, optimized for deployment on Vercel and supporting PostgreSQL (Neon).

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Vercel](https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## 📋 Features

- Full RESTful API for blog management
- Modular architecture with user, post, category, and comment systems
- Role-based authentication and permissions
- Compatible with SQLite (development) and PostgreSQL/Neon (production)
- Optimized for Vercel deployment
- CORS support and static file handling
- Custom admin panel
- Environment variables for flexible configuration

## 🔧 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for version control)
- Vercel account (for deployment)
- GitHub account (for repository)
- Neon or PostgreSQL account (for production database)

## 🚀 Installation & Setup

### Clone repository (or start from scratch)

```bash
# Clone the existing repository
git clone https://github.com/your-username/blogBackend.git
cd blogBackend

# Or create a new directory if starting from scratch
mkdir blogBackend
cd blogBackend
```

### Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate
```

### Install dependencies

```bash
pip install django djangorestframework django-cors-headers python-dotenv dj-database-url psycopg2-binary whitenoise gunicorn
pip freeze > requirements.txt
```

### Start project (if starting from scratch)

```bash
django-admin startproject core .
python manage.py startapp blog
```

### Configure environment variables

Create a `.env` file in the project root:

```
# General settings
DEBUG=True
SECRET_KEY=your_very_secure_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings (SQLite for local development)
DATABASE_URL=sqlite:///db.sqlite3

# For production with Neon
# DATABASE_URL=postgres://user:password@endpoint.neon.tech/dbname?sslmode=require
```

### Configure settings.py file

Edit `core/settings.py` to use the environment variables:

```python
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'blog',
]
```

### Run initial migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Run development server

```bash
python manage.py runserver
```

## 📁 Project structure

```
blogBackend/
│
├── core/                   # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URLs
│   └── wsgi.py             # Entry point for WSGI/Vercel
│
├── blog/                   # Main blog application
│   ├── __init__.py
│   ├── admin.py            # Admin panel configuration
│   ├── apps.py
│   ├── migrations/         # Database migrations
│   ├── models.py           # Data models (Post, Category, Comment)
│   ├── serializers.py      # API serializers
│   ├── tests.py            # Unit tests
│   ├── urls.py             # API URLs
│   └── views.py            # Views and ViewSets
│
├── scripts/                # Utility scripts
│   ├── setup.bat           # Setup script for Windows
│   └── setup.sh            # Setup script for Linux/Mac
│
├── venv/                   # Virtual environment (not versioned)
├── .env                    # Environment variables (not versioned)
├── .env.example            # Example of environment variables
├── .gitignore              # Files ignored by Git
├── build_files.sh          # Build script for Vercel
├── manage.py               # Django management tool
├── requirements.txt        # Project dependencies
├── vercel.json             # Vercel deployment configuration
└── README.md               # Main documentation
```

## 🌐 API Endpoints
- `POST /api-auth/login/` - Log in (Django REST Framework)
- `POST /api-auth/logout/` - Log out

## 🛠️ Data Models

### User (Django built-in)
- User management through Django's built-in model

## 🚀 Deploying to Vercel

### Prerequisites
- Vercel account
- Vercel CLI installed (optional)

### Vercel Configuration

The project includes a `vercel.json` file that sets up the environment for Vercel:


```json
{
  "version": 2,
  "builds": [
    {
      "src": "core/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    },
    {
      "src": "build_files.sh",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "staticfiles"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "core/wsgi.py"
    }
  ]
}
```

And a `build_files.sh` script to build static files:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

### Pasos para despliegue

1. **Configure Neon database**:
   - Create a database in Neon or a similar service
   - Copy the connection URL

2. **Setup environment variable in Vercel**:
   - `DEBUG`: False
   - `SECRET_KEY`: Secure secret key
   - `ALLOWED_HOSTS`: You Vercel domanin, e.g., blogbackend.vercel.app
   - `DATABASE_URL`: Neon connection URL
   - `CORS_ALLOWED_ORIGINS`: Allowed origins for CORS

3. **Deploy using CLI** (optional):

   ```bash
   vercel
   ```

4. **Or deploy using GitHub**:
   - Connect your repository to Vercel
   - Set environment variables
   - Automatically deploy on each push

## 📋 Implemented Best Practices

- **Configuration separation**: Use of environment variables to manage environment-specific settings
- **Modular architecture**: Clear separation of code into modules and apps
- **Data serialization**: Use of specific serializers per operation
- **Custom permissions**: Role-based permission system
- **Version control**: Git-friendly project structure
- **Security**: No credentials exposed in code
- **Documentation**: Complete README and self-documented code structure
- **Scalability**: Support for robust SQL databases

## 🧪 Testing

```bash
python manage.py test
```

## 📝 Post-installation
After the initial setup, consider the following tasks:

- **Create initial categories** through the admin panel
- **Configure permissions** according to your specific needs
- **Customize the admin panel** to enhance management experience
- **Implement specific tests** for your business logic
- **Set up a logging system** for production environments
- **Implement caching** to improve performance
- **Add a more advanced search system** if needed

## 🛣️ Next Steps and Possible Improvements

...

## 🤝 Contributions

...

## 📄 License

MIT License — see LICENSE file for more details.