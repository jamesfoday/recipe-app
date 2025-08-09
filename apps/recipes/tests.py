from django.test import TestCase
from django.urls import reverse
from apps.recipes.models import Recipe, RecipeIngredient
from apps.ingredients.models import Ingredient

class RecipeDetailViewTests(TestCase):
    def setUp(self):
        # Create ingredients
        ing1 = Ingredient.objects.create(name="Sugar", quantity="100g")
        ing2 = Ingredient.objects.create(name="Flour", quantity="200g")

        # Create recipe
        recipe = Recipe.objects.create(name="Cake", cooking_time=60, description="Delicious cake")

        # Link ingredients to recipe with quantities
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ing1, quantity="100g")
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ing2, quantity="200g")

    def test_recipe_detail_view_status_code(self):
        recipe = Recipe.objects.get(name="Cake")
        url = reverse('recipes:detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_ingredients_displayed(self):
        recipe = Recipe.objects.get(name="Cake")
        url = reverse('recipes:detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)
        self.assertContains(response, "Sugar")
        self.assertContains(response, "Flour")
