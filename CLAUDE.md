# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SS India Roofing** - A Django-based web application for a roofing company in Madurai, India. The application features:
- Public-facing website with product showcase, about section, and appointment booking
- Admin product management (CRUD) for staff users
- SQLite database for development

## Tech Stack

- **Framework**: Django 6.1.1
- **Database**: SQLite3 (db.sqlite3)
- **Frontend**: Bootstrap 5.3.8, Font Awesome 6.5.2, custom CSS/JS
- **Python**: 3.12 (via .venv)

## Project Structure

```
roof/
├── manage.py                 # Django management script
├── db.sqlite3                # SQLite database
├── .venv/                    # Virtual environment
├── ss_roofing/               # Project settings
│   ├── settings.py           # Main settings (DEBUG=False, ALLOWED_HOSTS configured)
│   ├── urls.py               # Root URLconf
│   ├── wsgi.py / asgi.py     # WSGI/ASGI entry points
├── roofing/                  # Main app
│   ├── models.py             # Product, Appointment models
│   ├── views.py              # Home, product CRUD views
│   ├── forms.py              # AppointmentForm, ProductForm
│   ├── urls.py               # App URL patterns
│   ├── admin.py              # Admin registration
│   └── migrations/           # Database migrations
├── templates/                # Global templates
│   ├── index.html            # Homepage with products, about, contact form
│   ├── product_list.html     # Admin product listing
│   ├── product_form.html     # Create/edit product form
│   └── product_confirm_deletion.html
├── static/
│   ├── css/style.css         # Custom styles (5.9KB)
│   └── js/script.js          # Client-side form validation
```

## Key Models

- **Product**: name, description, image (URLField)
- **Appointment**: first_name, last_name, city, phone, email, date, time, service, message

## Common Development Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows (Git Bash)

# Run development server
python manage.py runserver

# Create superuser for admin
python manage.py createsuperuser

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

## URL Routes

| Path | View | Name |
|------|------|------|
| `/` | `home` | `home` |
| `/admin/` | Django admin | - |
| `/manage/products/` | `product_list` | `product_list` |
| `/manage/products/add/` | `product_create` | `product_create` |
| `/manage/products/edit/<pk>/` | `product_update` | `product_update` |
| `/manage/products/delete/<pk>/` | `product_delete` | `product_delete` |

## Access Control

- **Public**: Home page, appointment booking
- **Staff only**: Product management (`/manage/products/`) - requires `user.is_staff` and authenticated via `@user_passes_test`

## Important Notes

1. **DEBUG=False** in settings.py - configured for production (PythonAnywhere deployment)
2. **ALLOWED_HOSTS** includes `ssroofing.pythonanywhere.com`
3. **Email backend**: Console backend (emails print to stdout)
4. **Static files**: Served from `static/` directory, collected to `staticfiles/` in production
5. **Image handling**: Product.image is a URLField (external URLs), not FileField
5. **Bug in views.py line 52**: `form.isvalid()` should be `form.is_valid()` - typo causes AttributeError on product update

## Templates Notes

- All templates extend no base template - each is a complete HTML document
- Bootstrap 5 loaded from CDN
- Custom CSS in `static/css/style.css`
- Appointment form has client-side validation in `static/js/script.js`

## Deployment Target

Configured for **PythonAnywhere** (see ALLOWED_HOSTS and DEBUG=False).