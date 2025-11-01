# 🚀 DEPLOYMENT – Chez Mama Restaurant Booking App

---

## 🧭 Overview

This document explains how the **Chez Mama Restaurant Booking App** was deployed to **Heroku** with **PostgreSQL** and **Cloudinary** integration.  
It also includes setup steps for running the project locally.

---

## 🌍 Live Site

🔗 **Live Application:**  
[https://restaurant-booking-vital-83aa0e106c92.herokuapp.com/](https://restaurant-booking-vital-83aa0e106c92.herokuapp.com/)

---

## 🧰 Technologies Used

| Component | Description |
|------------|-------------|
| **Backend** | Django 5.2.1 |
| **Database** | PostgreSQL (via Heroku Add-on) |
| **Media Storage** | Cloudinary |
| **Static Files** | Whitenoise |
| **Python Runtime** | 3.12.6 |
| **Deployment Platform** | Heroku |
| **Version Control** | Git & GitHub |

---

## 🧩 Pre-deployment Setup

Before deployment, ensure you have:
- A **GitHub** account (with your project repo)
- A **Heroku** account
- **Cloudinary** account (for media hosting)
- Installed:
  - [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
  - [Git](https://git-scm.com/)
  - [Python 3.12+](https://www.python.org/downloads/)

---

## ⚙️ 1. Preparing the Project

### Create `requirements.txt`

Freeze dependencies to ensure Heroku installs everything:

```bash
pip freeze > requirements.txt


### . Prepare Files

```bash

- `runtime.txt` (optional)

```
python-3.12.6
```

- `Collect Static Files` 

```
python manage.py collectstatic --noinput
```

Ensure these files exist:

- `Procfile`

```makefile
web: gunicorn restaurant_booking.wsgi
```

##🗄️ 2. Database Configuration

Locally, Django uses SQLite by default.
For production, the app uses PostgreSQL via the Heroku add-on.

Install and import:
```bash
pip install dj-database-url psycopg2-binary
```
In settings.py:
```bash
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))}
```

## ☁️ 3. Cloudinary Setup
Create a Cloudinary Account

Go to https://cloudinary.com/

Sign up for a free account

Copy your API Environment Variable (it looks like this):
CLOUDINARY_URL=cloudinary://xxxxxxxxxxxxxx

Add to .env or Heroku Config Vars
```dotev

CLOUD_NAME=your_cloud_name
CLOUD_API_KEY=your_api_key
CLOUD_API_SECRET=your_api_secret
```

Add to settings.py
```
python

INSTALLED_APPS = [
    ...,
    'cloudinary',
    'cloudinary_storage',
]

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('CLOUD_API_KEY'),
    'API_SECRET': config('CLOUD_API_SECRET'),
}

MEDIA_URL = '/media/'
```
## 🧱 4. Static Files Setup
Local Development
```
python

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Production

Whitenoise handles static file serving automatically:
```
python


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

```

Before deploying:
```
bash


python manage.py collectstatic --noinput

```

## 🔑 5. Environment Variables (.env)

Create a .env file in your project root (not committed to Git):
```
dotev

SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,restaurant-booking-vital-83aa0e106c92.herokuapp.com
CSRF_TRUSTED_ORIGINS=https://restaurant-booking-vital-83aa0e106c92.herokuapp.com

DATABASE_URL=postgres://user:password@hostname:port/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

## 6. Deploying to Heroku

### 1. Login & Create App

- Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Run `heroku login`
- Create a Heroku account

### 2. Create App and Database

```bash
heroku create your-app-name
```

### 3. Set Config Vars

```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=False
heroku config:set CLOUD_NAME=your_cloud_name
heroku config:set CLOUD_API_KEY=your_api_key
heroku config:set CLOUD_API_SECRET=your_api_secret
heroku config:set DATABASE_URL=your_database_url
heroku config:set ALLOWED_HOSTS=restaurant-booking-vital-83aa0e106c92.herokuapp.com
heroku config:set CSRF_TRUSTED_ORIGINS=https://restaurant-booking-vital-83aa0e106c92.herokuapp.com

```


### 4. Deploy

```bash
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main
heroku run python manage.py migrate
```

### 5. Create Admin User
```
bash

heroku run python manage.py createsuperuser
```

### 6.Collect Static Files
```
bash

heroku run python manage.py collectstatic --noinput
```

✅ Deployment complete!


### 🧪 7. Post-Deployment Checks
| Check               | Expected Result           | Status |
| ------------------- | ------------------------- | ------ |
| App loads via HTTPS | 200 OK                    | ✅      |
| Static files load   | Served by Whitenoise      | ✅      |
| Images load         | Served via Cloudinary     | ✅      |
| Database connected  | PostgreSQL active         | ✅      |
| Email sending       | SMTP confirmation working | ✅      |


### 💻 8. Running the App Locally
#### Clone the repository
```
bash
git clone https://github.com/vital-nsengiyumva/restaurant-booking.git
cd restaurant-booking
```
#### Create a virtual environment
```bash

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```
#### Install dependencies
```bash

pip install -r requirements.txt
```
#### Run migrations
```bash

python manage.py migrate
```
#### Create superuser
```bash

python manage.py createsuperuser
```
#### Start local server
```bash

python manage.py runserver
```
Then open http://127.0.0.1:8000.

#### 🧾 Troubleshooting Guide
| Issue                          | Possible Fix                                       |
| ------------------------------ | -------------------------------------------------- |
| `DisallowedHost` error         | Add `127.0.0.1` and Heroku URL to `ALLOWED_HOSTS`  |
| Static files not loading       | Run `collectstatic` again                          |
| Cloudinary upload error        | Verify API credentials in `.env`                   |
| “Missing manifest entry” error | Delete `staticfiles/` and re-run `collectstatic`   |
| 500 Server Error               | Temporarily set `DEBUG=True` locally to check logs |
| Email not sending              | Confirm SMTP credentials and app password in Gmail |


#### 🏁 Deployment Summary
| Step                   | Description                        | Status |
| ---------------------- | ---------------------------------- | ------ |
| Environment setup      | .env and decouple configured       | ✅      |
| Database migration     | Applied successfully               | ✅      |
| Static file collection | Whitenoise + Cloudinary functional | ✅      |
| Heroku deployment      | Successful (Gunicorn)              | ✅      |
| Cloudinary integration | Working for media                  | ✅      |
| SMTP email sending     | Working in production              | ✅      |

Chez Mama Restaurant Booking App



## 🧰 Local Setup (Development)

### 1. Clone the Repository
```bash
git clone https://github.com/vital-nsengiyumva/restaurant-booking.git
cd restaurant-booking

```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env File in the Project Root

dotev

SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000

#### Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

#### Database (if using PostgreSQL locally)
DATABASE_URL=postgres://user:password@host:port/dbname


### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

---

## 🌍 Deploying to Heroku
