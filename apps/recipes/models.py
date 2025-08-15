from django.db import models
from django.urls import reverse
from apps.ingredients.models import Ingredient

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField(help_text='Cooking time in minutes', null=True, blank=True)
    description = models.TextField(blank=True)
    pic = models.ImageField(upload_to='recipes/', blank=True)
    difficulty = models.CharField(max_length=10, choices=[('Easy','Easy'),('Medium','Medium'),('Hard','Hard')], default='Easy')
    created = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def calculate_difficulty(self):
        ingredient_count = self.recipe_ingredients.count()
        time = self.cooking_time if self.cooking_time is not None else 0

        if time < 30 and ingredient_count <= 5:
            return "Easy"
        elif (30 <= time <= 60) or (6 <= ingredient_count <= 10):
            return "Medium"
        else:
            return "Hard"

    def get_absolute_url(self):
        # matches the URL above (namespace: recipes, name: detail)
        return reverse("recipes:detail", args=[self.pk])    
def save_model(self, request, obj, form, change):
    super().save_model(request, obj, form, change)  # Save first to get primary key
    # Now calculate difficulty and save again if changed
    difficulty = obj.calculate_difficulty()
    if obj.difficulty != difficulty:
        obj.difficulty = difficulty
        obj.save(update_fields=['difficulty'])


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
