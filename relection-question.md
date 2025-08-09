# Exercise 2.4: Django Views and Templates - Reflection Questions

## 1. Explain how Django views work with an example

Django views are Python functions or classes that receive web requests and return web responses. They act as the "V" (View) in the Model-View-Template (MVT) architecture. The view handles the business logic, interacts with models if needed, and sends data to templates for rendering.

**Example:**

```python
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    context = {'message': 'Welcome to my Django app!'}
    return render(request, 'home.html', context)

 ## 2. Function-based views vs Class-based views for code reuse
When working on a Django project that requires reusing code in many places, class-based views (CBVs) are generally preferred because:

CBVs promote code reuse through inheritance and mixins.

They provide built-in generic views for common patterns (e.g., ListView, DetailView) which save development time.

They organize related logic in a class structure, making the code more modular and easier to maintain.

Function-based views (FBVs) are simpler and more explicit, but for large projects with reusable logic, CBVs provide better scalability and extensibility.

## 3. Notes on Django Template Language (DTL) basics
Django templates use variables wrapped in {{ }} to output dynamic content.

Control flow statements such as {% if %}, {% for %}, {% block %}, and {% extends %} allow logic and template inheritance.

Templates are HTML files enriched with DTL syntax to separate presentation from Python logic.

Filters (e.g., {{ value|lower }}) modify variables for display.

Custom template tags and filters can be created to extend functionality.


