# ✅ VALIDATION – Chez Mama Restaurant Booking App

---

## 🧭 Overview

This document presents validation evidence for **Chez Mama Restaurant Booking App**, confirming compliance with web standards and best practices.  
All validations were performed between **October–November 2025** on the latest deployed version hosted on Heroku:

🔗 [https://restaurant-booking-vital-83aa0e106c92.herokuapp.com/](https://restaurant-booking-vital-83aa0e106c92.herokuapp.com/)

---

## 🧩 HTML Validation

**Tool Used:** [W3C HTML Validator](https://validator.w3.org/nu/)  
**Pages Tested:**
- Home page (`/`)

    ![W3 home page validation - result: Passed](./media/validation_images/html_validation/home_page_valid.png)

- Booking form (`/book/`)

    ![book home page validated -result:passed](./media/validation_images/html_validation/book_page_validated.png)

- Menu page (`/menu/`)

    ![meu page validated by w3 - result - passed](./media/validation_images/html_validation/menu_page_validated.png)

- About us page (`/about/`)

    ![about us page passed validation](./media/validation_images/html_validation/about_page_validated.png)

- Contact page (`/contact/`)
    ![contact us page passed w3 validation](./media/validation_images/html_validation/contact_us_page_validated.png)

- My booking - only available for loged in users (`/my-booking/`)

    ![My booking page - only available for loged in users - passed w3 validation](./media/validation_images/html_validation/my_booking_page_validated.png)

- Login(`/accounts/login/`)

    ![login page passed w3 validation](./media/validation_images/html_validation/login_page_validated.png)

**Result:** ✅ **Passed**

**Notes:**
- No syntax or structural errors detected.
- All pages successfully render HTML5-compliant markup.

---

## 🎨 CSS Validation

**Tool Used:** [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

**File Validated:**  
- `/static/css/styles.css`

    ![css style sheet validated](./media/validation_images/css_validation/css_style_sheet_validated.png)

**Result:** ✅ **No errors found**

**Notes:**
- The file was confirmed to be free of invalid declarations and duplicate selectors.



## Lighthouse Checks

**Accessibility Checks using chrome Dev tool - Lighthouse**
- Home page accessibility

    ![home page accessibilty check](./media/validation_images/lighthouse_validation/home_page_validated_lighthouse.png)

    ![](./media/validation_images/lighthouse_validation/book_page_validated_lighthouse.png)

    ![](./media/validation_images/lighthouse_validation/about_us_page_lighthouse_validated.png)

    ![](./media/validation_images/lighthouse_validation/contact_us_page_validated_lighthouse.png)

    ![](./media/validation_images/lighthouse_validation/my_booking_page_validated_lighthouse.png)

♿ Accessibility


 Chrome DevTools Lighthouse (Desktop & Mobile)
| Category           | Score | Notes                                                 |
| ------------------ | ----- | ----------------------------------------------------- |
| **Performance**    | > 90%   | Static assets optimized via Whitenoise                |
| **Accessibility**  | > 90%   | Semantic HTML & ARIA roles correctly applied          |
| **Best Practices** | > 90%  | Secure HTTPS, valid image alt text, and clean console |
| **SEO**            | > 90%   | All pages include titles and meta descriptions        |
---

## 🐍 Python / PEP8 Validation

**Tool Used:**  
`flake8` and `pycodestyle` via terminal

**Command:**
```bash
python -m flake8

Files Tested:

- bookings/models.py

- bookings/forms.py

- bookings/views.py

- bookings/urls.py

- restaurant_booking/settings.py

Result: ✅ All files passed

Notes:

- No syntax, indentation, or import errors found.

- Minor line-length warnings (E501) ignored in long query chains for readability.

   

🌐 Responsiveness Validation

Tool Used: Chrome DevTools Responsive Viewer
| Device             | Resolution | Result       |
| ------------------ | ---------- | ------------ |
| Desktop            | 1920×1080  | ✅ Responsive |
| Laptop             | 1366×768   | ✅ Responsive |
| iPad               | 768×1024   | ✅ Responsive |
| iPhone 13          | 390×844    | ✅ Responsive |
| Samsung Galaxy S22 | 412×915    | ✅ Responsive |

✅ All layouts adjusted properly using Bootstrap 5.3 grid system and Flexbox.
No horizontal scroll or overlapping elements observed.


| Test                           | Expected                     | Result |
| ------------------------------ | ---------------------------- | ------ |
| Heroku app loads without error | Page served successfully     | ✅ Pass |
| Static files load correctly    | via Whitenoise               | ✅ Pass |
| Cloudinary image hosting       | Menu images display properly | ✅ Pass |
| Email configuration            | Confirmation emails work     | ✅ Pass |
| HTTPS enforced                 | All routes redirect securely | ✅ Pass |


🧾 Summary
| Validation Type | Tool Used            | Result |
| --------------- | -------------------- | ------ |
| HTML            | W3C Markup Validator | ✅ Pass |
| CSS             | W3C CSS Validator    | ✅ Pass |
| Python          | Flake8 / Pycodestyle | ✅ Pass |
| Accessibility   | Lighthouse           | ✅ Pass |
| Responsiveness  | Chrome DevTools      | ✅ Pass |
| Deployment      | Heroku / Cloudinary  | ✅ Pass |
