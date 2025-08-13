from django import forms
from .models import Recipe

class RecipeSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    ingredient = forms.CharField(required=False, label='Ingredient')
    max_cooking_time = forms.IntegerField(required=False, label='Max Cooking Time (minutes)')
    difficulty = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Any Difficulty'),
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
        ],
        label='Difficulty'
    )
    chart_type = forms.ChoiceField(
        required=False,
        choices=[('bar', 'Bar'), ('pie', 'Pie'), ('line', 'Line')],
        label='Chart Type'
    )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # NOTE: 'difficulty' is computed/non-editable -> do NOT include it here
        fields = ['name', 'cooking_time', 'description', 'pic']
