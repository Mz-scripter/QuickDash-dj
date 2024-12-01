import os
import django
from django.contrib.auth import get_user_model

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickdash.settings')
django.setup()

# Get the User model
User = get_user_model()

# Superuser details from environment variables
USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

def create_superuser():
    # Check if the superuser already exists
    if not User.objects.filter(username=USERNAME).exists():
        # Create superuser
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f'Superuser {USERNAME} created successfully')
    else:
        print(f'Superuser {USERNAME} already exists')

if __name__ == '__main__':
    create_superuser()
