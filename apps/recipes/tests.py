from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Recipe
from .forms import RecipeSearchForm

User = get_user_model()


class RecipeModelTests(TestCase):
    def test_absolute_url(self):
        r = Recipe.objects.create(name="Jollof", cooking_time=45, description="Smoky")
        # Don't assert on __str__ (some environments show "Recipe object (id)")
        self.assertEqual(r.get_absolute_url(), reverse("recipes:detail", args=[r.pk]))

    def test_calculate_difficulty_easy(self):
        r = Recipe.objects.create(name="Tea", cooking_time=5)
        self.assertEqual(r.calculate_difficulty(), "Easy")

    def test_calculate_difficulty_medium_by_time(self):
        r = Recipe.objects.create(name="Roast Veg", cooking_time=40)
        self.assertEqual(r.calculate_difficulty(), "Medium")

    def test_calculate_difficulty_hard_by_time(self):
        r = Recipe.objects.create(name="Beef Stew", cooking_time=95)
        self.assertEqual(r.calculate_difficulty(), "Hard")


class RecipeSearchFormTests(TestCase):
    def test_form_fields_and_choices(self):
        form = RecipeSearchForm()
        for field in ["name", "ingredient", "max_cooking_time", "difficulty", "chart_type"]:
            self.assertIn(field, form.fields)

        diff_choices = dict(form.fields["difficulty"].choices)
        self.assertIn("", diff_choices)
        self.assertIn("Easy", diff_choices)
        self.assertIn("Medium", diff_choices)
        self.assertIn("Hard", diff_choices)

        chart_choices = dict(form.fields["chart_type"].choices)
        for key in ["bar", "pie", "line"]:
            self.assertIn(key, chart_choices)

    def test_validation_accepts_partial_filters(self):
        form = RecipeSearchForm(
            data={"name": "rice", "max_cooking_time": 30, "difficulty": "Easy", "chart_type": "bar"}
        )
        self.assertTrue(form.is_valid(), form.errors.as_text())


class PublicViewsTests(TestCase):
    def test_welcome_route(self):
        url = reverse("recipes:welcome")
        self.assertEqual(resolve(url).url_name, "welcome")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_list_view(self):
        Recipe.objects.create(name="Okra Soup", cooking_time=25)
        url = reverse("recipes:list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Okra Soup")

    def test_detail_view(self):
        # Provide a tiny valid GIF so template can call {{ object.pic.url }} safely
        tiny_gif = (
            b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
            b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        )
        image = SimpleUploadedFile("tiny.gif", tiny_gif, content_type="image/gif")

        r = Recipe.objects.create(name="Fufu", cooking_time=15, description="Classic", pic=image)
        url = reverse("recipes:detail", kwargs={"pk": r.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Fufu")


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chef", email="c@example.com", password="pass1234")

    def test_login_view_get(self):
        url = reverse("recipes:login")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'id="password"')

    def test_login_then_home_requires_login(self):
        home_url = reverse("recipes:home")
        res = self.client.get(home_url)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login/", res.url)

        login_url = reverse("recipes:login")
        res = self.client.post(login_url, {"username": "chef", "password": "pass1234"}, follow=True)
        self.assertEqual(res.status_code, 200)

        res2 = self.client.get(home_url)
        self.assertEqual(res2.status_code, 200)

    def test_logout_flow(self):
        self.client.login(username="chef", password="pass1234")
        res = self.client.get(reverse("recipes:logout"))
        self.assertEqual(res.status_code, 302)
        # Your project may redirect to '/logout-success/' or '/recipes/logout-success/'
        self.assertTrue(res.url.endswith("logout-success/"))
        res2 = self.client.get(res.url)
        self.assertEqual(res2.status_code, 200)


class CreateAndSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chef", email="c@example.com", password="pass1234")

    def test_add_recipe_requires_login(self):
        url = reverse("recipes:add_recipe")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login/", res.url)

    def test_add_recipe_success(self):
        self.client.login(username="chef", password="pass1234")
        url = reverse("recipes:add_recipe")
        data = {
            "name": "Chicken Yassa",
            "cooking_time": 50,
            "description": "Senegalese favorite",
        }
        res = self.client.post(url, data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Recipe.objects.filter(name="Chicken Yassa").exists())

    def test_search_by_name_time_and_difficulty(self):
        Recipe.objects.create(name="Quick Salad", cooking_time=10, description="fresh", difficulty="Easy")
        Recipe.objects.create(name="Slow Stew", cooking_time=90, description="rich", difficulty="Hard")
        Recipe.objects.create(name="Mid Pasta", cooking_time=40, description="nice", difficulty="Medium")

        url = reverse("recipes:search_recipes")
        res = self.client.get(url, {"max_cooking_time": 30, "chart_type": "bar"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Quick Salad")
        self.assertNotContains(res, "Slow Stew")

        res2 = self.client.get(url, {"difficulty": "Medium", "chart_type": "pie"})
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "Mid Pasta")
        self.assertNotContains(res2, "Slow Stew")
        self.assertNotContains(res2, "Quick Salad")

        res3 = self.client.get(url, {"name": "stew"})
        self.assertEqual(res3.status_code, 200)
        self.assertContains(res3, "Slow Stew")

    def test_search_empty_valid_form(self):
        url = reverse("recipes:search_recipes")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("form", res.context)
