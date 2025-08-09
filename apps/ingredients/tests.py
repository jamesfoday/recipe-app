from django.test import TestCase
from django.urls import reverse
from .models import Ingredient

class IngredientViewTests(TestCase):
    def setUp(self):
        self.ing = Ingredient.objects.create(name="Salt", quantity="1 tsp")

    def test_ingredient_list_view(self):
        url = reverse('ingredients:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ing.name)

    def test_ingredient_detail_view(self):
        url = reverse('ingredients:detail', kwargs={'pk': self.ing.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ing.name)
        self.assertContains(response, self.ing.quantity)
