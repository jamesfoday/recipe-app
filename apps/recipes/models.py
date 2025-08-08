from django.db import models
from apps.ingredients.models import Ingredient

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField(help_text='Cooking time in minutes')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)  # e.g. "2 cups", "1 tsp"

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.name}"
