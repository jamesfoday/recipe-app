from django.db import models
from django.urls import reverse
from apps.ingredients.models import Ingredient

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField(help_text='Cooking time in minutes', null=True, blank=True)
    description = models.TextField(blank=True)
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg', blank=True)
    difficulty = models.CharField(max_length=20, blank=True, editable=False)  # Calculated automatically
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

    def save(self, *args, **kwargs):
        # Save the instance first to ensure it has a primary key
        super().save(*args, **kwargs)

        # Calculate difficulty after saving
        difficulty = self.calculate_difficulty()

        # Update difficulty if it has changed to avoid recursive saves
        if self.difficulty != difficulty:
            self.difficulty = difficulty
            # Update only the difficulty field to avoid recursion
            super().save(update_fields=['difficulty'])

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
