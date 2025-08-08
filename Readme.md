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

