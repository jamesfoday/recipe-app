# Learning Journal: Django Project Setup & Best Practices

**Date:** August 2025  
**Project:** Recipe Web Application with Modular Django Setup

---

### What I Did

- Created a **Django project** with a clean structure using a `config` folder for settings.  
- Implemented **environment-specific settings** by splitting configuration into `base.py` and `dev.py`.  
- Used **`.env` files** with `django-environ` for secure management of sensitive data like `SECRET_KEY`.  
- Organized apps inside an **`apps/` directory** for better project modularity (`recipes`, `ingredients`, `users`).  
- Created a **Makefile** to simplify common tasks such as running the server, creating apps, migrations, and running tests.  
- Learned how to **register apps correctly** and ensure proper import paths to avoid `ModuleNotFoundError`.  
- Used **`python manage.py migrate`** and **`python manage.py createsuperuser`** with custom settings.  
- Ensured all templates and views were correctly structured and linked.  
- Set up **version control readiness** with `.gitignore` and created a `requirements.txt` file to lock dependencies.  
- Practiced **running tests selectively** on specific apps or files via the Makefile.

---

### Challenges Faced

- Initial confusion with environment variable loading and `.env` file placement.  
- Errors related to app import paths (`apps.recipes` vs `recipes`).  
- Trouble using custom settings with Django management commands.  
- Template not found errors due to folder structure mismatch.  
- Proper setup of the `Makefile` to reflect the project's structure and environment.

---

### Key Takeaways

- **Separation of settings by environment** (base, dev, prod) increases project scalability and security.  
- Keeping apps inside an `apps/` folder helps keep the project root clean and improves maintainability.  
- `.env` files and `django-environ` are essential for handling sensitive config securely.  
- The `Makefile` can be a powerful tool to simplify repetitive Django commands.  
- Always verify `INSTALLED_APPS` paths and app configs to avoid import errors.  
- Running Django commands like `makemigrations` and `migrate` must be done from the project root (where `manage.py` is).  
- Proper template folder nesting is crucial for Django to find and render templates.

---

### Next Steps

- Implement models, views, and serializers for each app (`recipes`, `ingredients`, `users`).  
- Write unit and integration tests for core functionalities.  
- Add user authentication and permissions.  
- Set up deployment workflows (Heroku, Railway, etc.).  
- Explore API creation with Django REST Framework.  
- Automate tasks and CI/CD pipelines.

---
