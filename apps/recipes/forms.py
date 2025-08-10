from django import forms

DIFFICULTY_CHOICES = [
    ('', 'Any'),          # Allow no filter
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]

CHART_TYPE_CHOICES = [
    ('bar', 'Bar Chart'),
    ('pie', 'Pie Chart'),
    ('line', 'Line Chart'),
]

class RecipeSearchForm(forms.Form):
    name = forms.CharField(required=False, max_length=200, label='Recipe Name')
    ingredient = forms.CharField(required=False, max_length=100, label='Ingredient')
    max_cooking_time = forms.IntegerField(required=False, min_value=1, label='Max Cooking Time (minutes)')
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False)
    chart_type = forms.ChoiceField(choices=CHART_TYPE_CHOICES, required=False, initial='bar')
