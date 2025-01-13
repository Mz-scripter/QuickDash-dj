# QuickDash-dj
![Convenience Delivered, Every Time _ QuickDash](https://github.com/user-attachments/assets/e0f1835a-3a1e-4b67-a2d3-e5cb5e375910)

QuickDash is an online food ordering platform designed to offer a seamless experience for customers, sellers, and restaurant owners. This Django-based project integrates robust features like authentication, search, cart management, distance calculation, and more.

## Features

### Customer Features
- User Authentication:
    - Register, login and logout functionality.
    - Password reset and email verification for secure access.
- Product Management:
    - Browse food items by restaurant or search queries.
    - Autocomplete search for enhanced user experience.
    - Add items to the cart or a wish list for future purchases.
- Cart Management:
    - Add, update, or remove items from the cart.
    - View total quantities and prices in the cart.
- Distance Calculation:
    - View the distance from the restaurant to the user’s location or address.

### Seller Features
- Profile Management:
    - Update personal information like name, address, and phone number.
    - Register as a seller and manage uploaded items.
- Product Listing:
    - Add new food items with details such as price, image, description, and restaurant.

### Restaurant Features
- Restaurant Management:
    - Link items to restaurants for organized searches.
    - Add new restaurants and manage related products.

## Setup Instructions
### Requirements
- Python 3.8 or above
- Django 4.x
- PostgreSQL or SQLite database
- Mapbox or another geolocation service for distance calculation

## Local Development
1. Clone the repository
```
git clone https://github.com/Mz-scripter/QuickDash-dj.git
```
2. Set up a virtual environment
```
python -m venv env
source venv/Scripts/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Configure environment variables
Create a `.env` file in the root directory and add the following:
```
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
```
5. Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
6. Collect static files
```
python manage.py collectstatic
```
7. Run the development server
```
python manage.py runserver
```
8. Create superuser
```
python manage.py createsuperuser
```
