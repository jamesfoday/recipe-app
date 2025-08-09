from django.db import models
from django.urls import reverse
from apps.ingredients.models import Ingredient

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField(help_text='Cooking time in minutes', null=True, blank=True)
    description = models.TextField(blank=True)
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg', blank=True)
    difficulty = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)  # e.g. "2 cups", "1 tsp"

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.name}"
