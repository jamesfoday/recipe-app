from django.urls import path
from .views import (
    welcome,
    home,
    about,
    RecipeListView,
    RecipeDetailView,
    login_view,
    logout_view,
    logout_success,
    search_recipes,  # import your search view here
    RecipeCreateView,
)

app_name = 'recipes'

urlpatterns = [
    path('', welcome, name='welcome'),
    path('home/', home, name='home'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='detail'),

    # Authentication routes
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout-success/', logout_success, name='logout_success'),

    # Search route - make sure name matches the test
      path('search/', search_recipes, name='search_recipes'),# <-- changed here
    path('about/', about, name='about'),
    path('add/', RecipeCreateView.as_view(), name='add_recipe'),

]
