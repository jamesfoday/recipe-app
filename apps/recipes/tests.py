from django.test import TestCase
from django.urls import reverse
from apps.recipes.models import Recipe, RecipeIngredient
from apps.ingredients.models import Ingredient
from django.contrib.auth.models import User
from .forms import RecipeSearchForm

class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.ing1 = Ingredient.objects.create(name="Sugar")
        self.ing2 = Ingredient.objects.create(name="Flour")
        self.recipe = Recipe.objects.create(name="Cake", cooking_time=60, description="Delicious cake")
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ing1, quantity="100g")
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ing2, quantity="200g")

    def test_recipe_detail_view_status_code(self):
        url = reverse('recipes:detail', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_ingredients_displayed(self):
        url = reverse('recipes:detail', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)
        self.assertContains(response, "Sugar")
        self.assertContains(response, "Flour")

class RecipeSearchFormTests(TestCase):
    def test_form_accepts_valid_data(self):
        form_data = {
            'name': 'Chicken',
            'ingredient': 'Garlic',
            'max_cooking_time': 30,
            'difficulty': 'Easy'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_negative_cooking_time(self):
        form_data = {'max_cooking_time': -10}
        form = RecipeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_all_fields_optional(self):
        form = RecipeSearchForm(data={})
        self.assertTrue(form.is_valid())

class SearchRecipesViewTests(TestCase):
    def setUp(self):
        self.url = reverse('recipes:search_recipes')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.garlic = Ingredient.objects.create(name='Garlic')
        self.chicken_recipe = Recipe.objects.create(name='Garlic Chicken', cooking_time=25, description='Tasty garlic chicken')
        RecipeIngredient.objects.create(recipe=self.chicken_recipe, ingredient=self.garlic, quantity='2 cloves')

    def test_search_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_search_by_name_returns_correct_recipe(self):
        response = self.client.get(self.url, {'name': 'Garlic'})
        self.assertContains(response, 'Garlic Chicken')

    def test_search_by_ingredient_returns_correct_recipe(self):
        response = self.client.get(self.url, {'ingredient': 'Garlic'})
        self.assertContains(response, 'Garlic Chicken')

    def test_search_no_results(self):
        response = self.client.get(self.url, {'name': 'NoSuchRecipe'})
        self.assertContains(response, 'No recipes found.')

    def test_search_renders_chart(self):
        response = self.client.get(self.url, {'name': 'Garlic', 'chart_type': 'bar'})
        self.assertContains(response, '<img', status_code=200)

class LoginViewTests(TestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('recipes:home'))

    def test_login_fail(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertContains(response, 'Ooops... something went wrong.')
