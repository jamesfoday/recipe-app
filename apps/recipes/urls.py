from django.urls import path, include
from apps.recipes.views import home, welcome, RecipeListView , RecipeDetailView

app_name = 'recipes'


urlpatterns = [
    path('', welcome, name='welcome'),      
    path('home/', home, name='home'), 
    path('list/', RecipeListView.as_view(), name='list'),  # /list/ for recipe list
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='detail'), 
     path('ingredients/', include('apps.ingredients.urls')),
]
