# 🧪 TESTING – Chez Mama Restaurant Booking App

---

## 🧭 Overview

This document details all **manual and automated tests** performed for the **Chez Mama Restaurant Booking App**.  
It includes testing of **CRUD operations**, **authentication**, **defensive design**, **responsiveness**, **validation**, and **deployment verification**.

Testing was conducted in both:
- 🧩 **Local development** (`DEBUG=True`)
- ☁️ **Heroku production** (`DEBUG=False`)

---

## ✅ Summary of Test Results

| Category | Result | Notes |
|-----------|--------|-------|
| CRUD functionality | ✅ Pass | Full Create, Read, Update, Delete cycle works |
| Authentication | ✅ Pass | Registration, login, logout verified |
| Defensive design | ✅ Pass | Unauthorized access blocked |
| Booking form | ✅ Pass | Prevents double-bookings and invalid dates |
| Table allocation | ✅ Pass | Automatically assigns smallest available table |
| Feedback form | ✅ Pass | Submits ratings and comments successfully |
| Menu pagination | ✅ Pass | Works across all browsers |
| Email confirmation | ✅ Pass | SMTP + console email verified |
| Static files | ✅ Pass | Loaded via Whitenoise & Cloudinary in production |
| Responsiveness | ✅ Pass | Tested on desktop, tablet, and mobile |
| Deployment | ✅ Pass | Heroku live deployment successful |

---

## 🧱 Manual Testing Details

### 1️⃣ CRUD Functionality

| Action | Steps | Expected Result | Actual Result | Status |
|--------|-------|-----------------|----------------|--------|
| **Create Booking** | Fill public booking form with name, email, date, time | Booking saved & confirmation displayed | Booking saved, confirmation email shown | ✅ |
| **Read Booking** | View in admin panel or “My Bookings” page | All user bookings visible | Works as expected | ✅ |
| **Update Booking** | Modify booking from dashboard | Changes saved in DB | Updates reflected immediately | ✅ |
| **Delete Booking** | Click cancel button | Booking removed | Removed from list, success message shown | ✅ |
| **Cancel Booking via Token** | Click link in email | Booking cancelled | Status set to “cancelled” in DB | ✅ |

---

### 2️⃣ Authentication Tests

| Scenario | Steps | Expected Result | Actual Result | Status |
|-----------|-------|-----------------|----------------|--------|
| **Register user** | `/accounts/register/` | Redirects to home | Works | ✅ |
| **Login user** | `/accounts/login/` | Redirect to “My Bookings” | Works | ✅ |
| **Logout user** | Click logout | Redirect to home | Works | ✅ |
| **Invalid login** | Wrong password | Error message displayed | Works | ✅ |
| **Access protected page while logged out** | Visit `/bookings/1/` | Redirect to login | Works | ✅ |

---

### 3️⃣ Defensive Design

| Scenario | Attempt | Expected Response | Actual Response | Result |
|-----------|----------|------------------|----------------|---------|
| Edit another user’s booking | Change booking ID in URL | Access denied | Redirected to home | ✅ |
| Submit invalid date | Choose past date | Error shown | Form validation blocks it | ✅ |
| Double booking same table/time | Two users same slot | Error shown | Prevented by `unique_together` rule | ✅ |
| Invalid phone/email | Submit with letters or wrong format | Validation error | Error displayed inline | ✅ |

---

### 4️⃣ Form Validation

| Form | Field | Validation | Result |
|------|--------|-------------|--------|
| Public Booking | Email | Must be valid email format | ✅ |
| Public Booking | Phone | Digits only (Regex) | ✅ |
| Public Booking | Date | Future dates only | ✅ |
| Feedback | Rating | Must be numeric 1–5 | ✅ |
| Contact Form | Email | Must be valid | ✅ |

---

### 5️⃣ Menu Page

| Test | Steps | Expected | Result |
|------|--------|-----------|--------|
| Pagination | Scroll through menu pages | 3 items per page | ✅ |
| Image load | Menu item has Cloudinary image | Image loads quickly | ✅ |
| “Book this dish” link | Click dish button | Opens booking form with pre-filled menu item | ✅ |

---

### 6️⃣ Responsiveness Testing

| Device | Browser | Display | Status |
|--------|----------|----------|--------|
| 💻 Desktop (1920×1080) | Chrome, Edge | Fully responsive | ✅ |
| 💻 Laptop (1366×768) | Firefox | Layout holds correctly | ✅ |
| 📱 iPhone 13 | Safari | Navbar collapses into menu | ✅ |
| 📱 Samsung Galaxy | Chrome Mobile | Booking form responsive | ✅ |
| 📱 iPad | Safari | Columns align properly | ✅ |

---

## 💬 Feedback Form Testing

| Step | Expected | Actual | Result |
|------|-----------|--------|--------|
| Submit rating/comment | Saved in database | Saved successfully | ✅ |
| Leave comment blank | Accepts rating only | Works | ✅ |
| Invalid rating | Rejects value outside 1–5 | Blocked | ✅ |

---

## 🌍 Deployment Verification (Heroku)

| Test | Expected Outcome | Actual Result | Status |
|------|------------------|----------------|--------|
| Load home page | Loads without errors | ✅ Works |
| Static files | Loaded from `/staticfiles/` | ✅ Works |
| Media files | Served via Cloudinary | ✅ Works |
| Email sending | Confirmation email sent | ✅ Works |
| Booking form | Submits and stores booking | ✅ Works |
| Cancel booking | Updates status | ✅ Works |

---

## 🔒 Environment & Settings Tests

| Setting | Description | Checked | Result |
|----------|--------------|----------|--------|
| `DEBUG=True` (local) | Console email backend | ✅ Works |
| `DEBUG=False` (Heroku) | SMTP email backend | ✅ Works |
| `STATIC_ROOT` | `staticfiles/` folder created after `collectstatic` | ✅ Works |
| `STORAGES` | Cloudinary + Whitenoise configuration | ✅ Works |
| `.env` Variables | Loaded via python-decouple | ✅ Works |

---

## 🧩 Validation Testing

### ✅ HTML Validation
Tested all rendered templates using **W3C HTML Validator**  
🔹 All templates passed with **no critical errors**  
Minor warnings (like Bootstrap ARIA roles) safely ignored.

### ✅ CSS Validation
Validated via **W3C CSS Validator**  
🔹 `styles.css` passed without syntax errors.

### ✅ Python Validation
Used:
```bash
python -m flake8



## 🧪 Automated Testing - optional and did not do it yet by the submission time

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



Result:
✅ No syntax or indentation errors found.
Minor style warnings (line length > 79) ignored for readability.

✅ Accessibility / Lighthouse

Tested using Chrome DevTools Lighthouse report:
| Category       | Score |
| -------------- | ----- |
| Performance    | 93%   |
| Accessibility  | 96%   |
| Best Practices | 100%  |
| SEO            | 98%   |

🐞 Known Issues (as of current release)
| Issue                  | Description                                     | Workaround                    |
| ---------------------- | ----------------------------------------------- | ----------------------------- |
| Image refresh in admin | Uploaded menu images may not appear instantly   | Refresh page                  |
| Mobile layout          | Some images slightly overlap on smaller screens | Adjust Bootstrap grid later   |
| Cancellation email     | Not yet implemented                             | To be added in next sprint    |
| Booking time overlap   | Rare edge case if simultaneous form submission  | Acceptable limitation for MVP |


🧪 Future Testing (Planned)
Automated tests using pytest-django

Selenium browser tests for live booking and cancellation

Unit tests for views (public_booking_view, cancel_booking_view)

Email delivery tests (mock SMTP)

Cloudinary upload integration test

🧰 Testing Environment Summary
| Component   | Version                      |
| ----------- | ---------------------------- |
| Django      | 5.2.1                        |
| Python      | 3.12.6                       |
| Bootstrap   | 5.3.3                        |
| PostgreSQL  | 16 (Heroku)                  |
| Cloudinary  | Active                       |
| Debug Tools | Django Debug Toolbar (local) |


✅ Final Test Conclusion

All major functionalities of the Chez Mama Restaurant Booking App have been thoroughly tested both locally and in production.

All critical tests passed successfully, including:

CRUD operations

Authentication and defensive design

Static/media file serving

Email confirmation

Cloudinary integration

Deployment stability

---

Chez Mama Restaurant Booking App


