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
        # Save the object first to get a primary key
        super().save_model(request, obj, form, change)

        # Calculate difficulty after save
        difficulty = obj.calculate_difficulty()

        # Update difficulty if changed
        if obj.difficulty != difficulty:
            obj.difficulty = difficulty
            obj.save(update_fields=['difficulty'])
