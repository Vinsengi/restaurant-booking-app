# 🍽️ Chez Mama Restaurant Booking App
![Am I responsive Images](bookings\static\bookings\images\Amiresponsive.png)
- [Live Appliction](https://restaurant-booking-vital-83aa0e106c92.herokuapp.com/)
---

# 🍽️ Restaurant Booking Website

Welcome to our **Restaurant Booking Website**! A full-featured web application for a restaurant that allows visitors to::

- 📜 Browse our traditional Rwandan meals on our menu of delicious dishes with a pagination 
- 🍽️ Book a table online and even choose your dish in advance  
- 📧 Get email confirmation when your booking is successful  

Built with love and powered by Django, it’s here to make your dining experience smooth and simple.


## 🎯 Purpose

This app is designed to help small and medium-sized restaurants:
- Accept and manage table reservations online.
- Display an interactive and image-rich menu.
- Automate table availability checks to avoid double-bookings.
- Store and serve images reliably through Cloudinary.

---

## 🚀 Features

- **Menu listing**: Menu items stored in a database (with image support and availability).
- **Booking system**: Users can book a table based on the number of guests and optionally book a specific dish.
- **Admin panel**: Full Django admin for managing bookings, menu items, and customer feedback.
- **Image uploads**: Media support for dish images.
- **Email notifications**: Configurable SMTP setup for email confirmation.
- **Responsive UI**: Clean layout using Bootstrap classes.
- **Pagination**: Menu items are paginated for a better user experience.
- ** etc.

---

---

## 📦 Other Features

- ✅ Public booking form with live table availability
- ✅ Automatic table assignment based on number of guests
- ✅ Menu with image upload and Cloudinary integration
- ✅ Prevents double bookings for the same table/date/time
- ✅ Stores customer details with duplicate-check logic

---
## 🛠️ Technologies Used

- Django 5.2.1
- PostgreSQL (for production) / SQLite (for development)
- HTML/CSS (Bootstrap 5)
- Python 3.12
- [python-decouple](https://github.com/HBNetwork/python-decouple)
- [whitenoise](http://whitenoise.evans.io/en/stable/) for static file handling

---

## 📦 Setup Instructions (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/restaurant-booking.git
cd restaurant-booking
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```dotenv
SECRET_KEY=your_django_secret_key
DEBUG=True

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

# PostgreSQL (used by Heroku)
DATABASE_URL=postgres://user:password@host:port/dbname
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

---

## 🌍 Deploying to Heroku

### 1. Prerequisites

- Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Run `heroku login`
- Create a Heroku account

### 2. Setup Heroku

```bash
heroku create your-app-name
```

### 3. Add Heroku PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 4. Set Environment Variables on Heroku

```bash
heroku config:set SECRET_KEY=your_django_secret_key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Email variables
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER=your_email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your_app_password
heroku config:set DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### 5. Prepare for Heroku

Ensure these files exist:

- `Procfile`

```makefile
web: gunicorn restaurant_booking.wsgi
```

- `requirements.txt`

```bash
pip freeze > requirements.txt
```

- `runtime.txt` (optional)

```
python-3.12.6
```

### 6. Deploy

```bash
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main
```

### 7. Run Migrations on Heroku

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 📸 Traditional Dishes in the Menu

The app highlights dishes such as:

- Isombe 🥬
- Akabenz 🐖
- Ubugali 🍚
- Ibihaza 🎃
- Melange 🍲
- Ibirayi 🍟
- etc.

Each is displayed with consistent image styling and pagination for better UX.

---

## 📧 Email Notifications

The system is configured to send confirmation emails upon successful bookings using SMTP credentials.

Email comes with a cancellation link.

if user choses to cancel the booking, they will be asked if they are sure, and if they are, they will cancel and a cancellation-success will be shown.

---

## 🗂 Project Structure

```bash
restaurant_booking/
│
├── bookings/              # Main app
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/bookings/
│
├── media/                 # Dish images
├── static/                # CSS, JS, images
├── .env                   # Environment secrets (not committed)
├── Procfile
├── requirements.txt
└── manage.py
```

---

## 📦 Setup Instructions (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/restaurant-booking.git
cd restaurant-booking
```

# 🍽️ Django Restaurant Booking App with Cloudinary Integration

This is a web-based restaurant booking system built using Django. It features a public booking interface, a live table availability checker, a visual menu with images hosted on Cloudinary, and an admin panel for managing bookings and menu items.

---

## 🍴 Fork This Project

1. **Fork this repository** using the GitHub UI.
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/your-forked-repo.git
   cd your-forked-repo
   ```

3. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up Cloudinary:**
   Add these credentials to a `.env` file or your `settings.py`:
   ```env
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

5. **Apply migrations and run server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## ⚙️ Cloudinary Configuration

In `settings.py`, add:

```python
INSTALLED_APPS = [
    ...
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    ...
]

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your_cloud_name',
    'API_KEY': 'your_api_key',
    'API_SECRET': 'your_api_secret',
}

MEDIA_URL = '/media/'
```

---

## 📁 Models Overview

Example `MenuItem` model:

```python
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
```

---

## ✅ Manual Testing

| Feature                    | Steps                                                                 |
|---------------------------|-----------------------------------------------------------------------|
| Booking                   | Visit `/book/` and complete the form. Check DB/admin for record.     |
| Duplicate Prevention      | Try booking same table/date/time twice — should be blocked.          |
| Cancel Booking            | Use `/cancel/` to enter details and verify it's removed.             |
| Menu Image Display        | Upload a menu item with an image and verify it shows on `/menu/`.    |

---

## 🧪 Automated Testing

Run all tests with:

```bash
python manage.py test
```

Example test:

```python
from django.test import TestCase
from .models import Booking

class BookingTestCase(TestCase):
    def test_booking_creation(self):
        booking = Booking.objects.create(name='John', email='john@example.com', ...)
        self.assertEqual(Booking.objects.count(), 1)
```

Use `unittest.mock` or `pytest-django` to simulate image uploads if needed.

---

## 🧰 Deployment Notes

To deploy this project:
- Ensure all Cloudinary credentials are added to the environment.
- Use Heroku or any cloud service with Django + PostgreSQL support.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in production.

---

## 🙋 Contributing

Contributions are welcome! Please fork the repository, create a new branch, and open a pull request with your improvements or fixes.



---

## 🚀 Features Planned for the Next Release

Here are upcoming improvements and features planned for the next version of the app:

- 🔄 **Real-time table availability preview**: Show live feedback to users about available time slots before submitting the booking form.
- 📨 **Email notifications**: Send cancellation emails to customers automatically after thy cancel.
- 📱 **Responsive UI improvements**: Improve the mobile layout and form usability on small screens.
- 🌐 **Multilingual support**: Add basic internationalization (i18n) starting with English and French.
- 🔐 **Admin role permissions**: Introduce finer-grained permissions to allow different admin roles.
- 🗓️ **Calendar view for admin bookings**: Add a calendar-style UI to visualize daily bookings.
- 💬 **Customer feedback form improvements**: Include rating stars and comment moderation in the feedback system.
- ⚙️ **Optional table selection**: Let repeat customers optionally select a preferred table if available.
- 📅 ** Add and display date and time the restaurant is open. currently, the assumption is that it is 24/7 open and ready to serve customers.
- 🗺️ ** Add map fucntionaly
- 💳💶 ** online ordering and Add payment functionalities

Stay tuned and watch the GitHub repo for upcoming milestones and issues.

---

## 🐞 Known Bugs

The following issues have been identified and are under review:

- ❗ **Image not uploading to Cloudinary**: In some setups, images appear broken because of Cloudinary issues.
- ⚠️ **Admin panel menu image preview**: Uploaded images sometimes don’t render in the admin panel preview after saving — requires manual refresh.
- 🕐 **Booking time slot conflicts**: In rare race conditions, double bookings may occur if two users submit forms simultaneously.
- 📧 **Missing cancellation email confirmation**: Cancellation emails are not yet implemented, so users do not receive acancellation email receipt.
- 📆 **Date/time picker browser incompatibility**: Some mobile browsers render the date/time input fields inconsistently.
- 📱 **Menu layout on small screens**: Menu items and images may overlap or stack poorly on very narrow screens.

These bugs are documented and will be addressed in future releases. Contributions and bug reports are welcome via GitHub Issues.

---

## 🧩 Agile Development Approach

This project follows Agile development principles to ensure continuous delivery, transparency, and adaptability. Key practices include:

- 📅 **Iterative Releases**: The app evolves through clearly defined development phases (sprints), each delivering working features.
- 📋 **Backlog Grooming**: New features, bugs, and improvements are maintained in a prioritized backlog for review each sprint.
- 👥 **User Stories**: Development tasks are based on user stories that reflect real needs of restaurant customers and admins.
- 🔁 **Continuous Feedback**: Manual and automated testing at the end of each sprint ensures feedback loops are fast and relevant.
- 🔄 **Flexibility**: The product roadmap adapts based on testing results, user experience insights, and stakeholder input.

This approach helps the team stay focused on delivering business value quickly while keeping the project highly maintainable and user-centered.


## 🖥️ For Non-Developers: How This Was Built

This website was created using a platform called **Django** (a tool developers use to build websites). It connects to a database that stores all our dishes and booking details.

- Your bookings are saved securely  
- Dish pictures are added by the admin team  
- Emails are sent automatically when you book

---

## 🚀 How We Shared This Site with the World (Deployment)

We used **Heroku**, a hosting service, to put the website online. Think of it like putting our restaurant on Google Maps – now everyone can find and use it!

Steps involved:
1. We signed up on Heroku
2. Connected our website to Heroku
3. Set up the database and email settings there
4. Published it online

---

## 🗂️ About the Menu Page

On the **menu page**, you’ll find:
- Paginated list (like flipping pages of a photo album)
- Dish names and pictures
- “Book this dish” buttons, so you can reserve your favorite easily

---

## 📧 About Email Confirmation

When you book:
- An email is sent automatically to confirm your reservation
- It includes your name, booking time, and selected dish (if any)

---

## 🌍 Want to Help or Share Ideas?

You can reach out to the admin team with suggestions, traditional dish ideas, or feedback. We’d love to improve the experience!

Thank you for visiting our restaurant site – enjoy your meal! 🇷🇼🍛

---

## 🧰 Complete Local Setup Guide

### 1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the root directory:

```dotenv
SECRET_KEY=your_django_secret_key
DEBUG=True

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

# PostgreSQL (used by Heroku)
DATABASE_URL=postgres://user:password@host:port/dbname
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

---

## 🗂 Project Structure in brief 

```bash
restaurant_booking/
│
├── bookings/              # Main app
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/bookings/
│
├── media/                 # Dish images
├── static/                # CSS, JS, images
├── .env                   # Environment secrets (not committed)
├── Procfile
├── requirements.txt
└── manage.py
```

---

## ✅ Future Enhancements

- User authentication
- Dish rating and reviews
- Admin notifications
- Multilingual support

## 🤝 Credit and Aknowledgments

- Inspired by traditional Rwandan cuisine and culture.

- Thanks to the Django community and contributors.

- Special thanks to the Equip-Magu initiative for educational empowerment for allowing us to use the website as a fall-back during the construction of chez mama restaurant's website.