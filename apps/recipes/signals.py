from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RecipeIngredient, Recipe

@receiver([post_save, post_delete], sender=RecipeIngredient)
def update_recipe_difficulty(sender, instance, **kwargs):
    recipe = instance.recipe
    recipe.difficulty = recipe.calculate_difficulty()
    recipe.save()
