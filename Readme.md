# My Recipe Project

A Django-based web application for managing recipes, ingredients, and users with a clean, scalable project structure.

---

## Project Structure

- `config/` - Django project configuration folder containing:
  - `settings/` - Separate settings modules (`base.py`, `dev.py`, etc.)
  - `urls.py`, `wsgi.py`, `asgi.py`
- `apps/` - Django applications folder containing:
  - `recipes/` - Recipes app
  - `ingredients/` - Ingredients app
  - `users/` - Users app
- `.venv/` - Python virtual environment (excluded from Git)
- `manage.py` - Django management script
- `Makefile` - Command shortcuts for development
- `.env` - Environment variables (not committed to repo)
- `requirements/` - Requirement files for base and dev environments

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd my_recipe_project

### 2. Create and activate the virtual environment

python3 -m venv .venv
source .venv/bin/activate

### 3. Install dependencies
pip install -r requirements/dev.txt

### 4. Setup environment variables
Create a .env file in the project root with the following content (example): SECRET_KEY=your_secret_key_here
DEBUG=True

### 5. Run migrations
python manage.py migrate --settings=config.settings.dev

### 6. Create super user
python manage.py createsuperuser --settings=config.settings.dev

###7 run development server
python manage.py runserver

# 🍽️ Recipe App

A Django-based recipe management platform where users can browse, search, and add recipes.  
Includes authentication, search filtering, difficulty calculation, and chart visualizations.  
Built with a modular structure for scalability and integrated with **Cloudinary** for image storage.

---

## ✨ Features

- **User Authentication**
  - Login, logout, and restricted home page.
  - Customizable password input styling.

- **Recipe Management**
  - Create, view, update, and delete recipes.
  - Upload images for each recipe (`pic` field) — stored on **Cloudinary**.
  - Automatic difficulty calculation based on cooking time and ingredients.

- **Search & Filters**
  - Search by name, ingredient, max cooking time, and difficulty.
  - Generate charts (`bar`, `pie`, `line`) based on search results.

- **Responsive Views**
  - Welcome page for guests.
  - Recipe list and detail pages.
  - Search results with visual charts.

- **Cloudinary Integration**
  - All uploaded recipe images are stored and served from Cloudinary.

- **Test Coverage**
  - Unit tests for models, forms, and views in a single test file.
  - Easily extendable test suite.

---

## 🗂 Project Structure

Recipe-app/
├── apps/
│ └── recipes/
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── models.py
│ ├── forms.py
│ ├── views.py
│ ├── urls.py
│ ├── tests.py
│ └── ...
├── config/
│ ├── settings/
│ │ ├── base.py
│ │ ├── dev.py
│ │ └── prod.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md


---

## 🛠 Tech Stack

- **Backend:** Django 5.x
- **Database:** PostgreSQL (or SQLite for development)
- **Media Storage:** Cloudinary
- **Frontend:** Django templates + static CSS
- **Charts:** Matplotlib (via custom chart generator)
- **Testing:** Django `TestCase`

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/jamesfoday/recipe-app
cd recipe-app

### . Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

### .  Install dependencies
pip install -r requirements.txt

### .  Create a .env file at the project root:

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/recipe_db

# Cloudinary
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>

### . Run migrations
python manage.py migrate --settings=config.settings.dev

### . Create a superuser
python manage.py createsuperuser --settings=config.settings.dev


### . Run the development server
make test
# or
python manage.py test --settings=config.settings.dev

### . Deployment
heroku create my-recipe-app
heroku config:set DJANGO_SECRET_KEY=...
heroku config:set CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
git push heroku main
