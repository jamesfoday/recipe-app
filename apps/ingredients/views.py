from django.views.generic import ListView, DetailView
from .models import Ingredient

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/list.html'  # Create this template

class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'ingredients/detail.html'  # Create this template
