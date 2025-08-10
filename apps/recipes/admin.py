from django.contrib import admin
from .models import Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'cooking_time', 'difficulty']
    readonly_fields = ['difficulty']

    def save_model(self, request, obj, form, change):
        # Automatically calculate difficulty before saving
        obj.difficulty = obj.calculate_difficulty()
        super().save_model(request, obj, form, change)
