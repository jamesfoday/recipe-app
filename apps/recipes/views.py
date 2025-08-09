from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Recipe

def welcome(request):
    return render(request, 'welcome.html')  # project-level templates/welcome.html

def home(request):
    return render(request, 'recipes/home.html')  # app-level templates/recipes/home.html

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'  # you can reuse home.html as the list page

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'  # create this template next    
