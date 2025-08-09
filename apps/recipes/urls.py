from django.urls import path
from apps.recipes.views import (
    welcome,
    home,
    RecipeListView,
    RecipeDetailView,
    login_view,
    logout_view,
    logout_success,
)

app_name = 'recipes'

urlpatterns = [
    path('', welcome, name='welcome'),
    path('home/', home, name='home'),
    path('list/', RecipeListView.as_view(), name='list'),  # recipe list page
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='detail'),  # recipe detail page

    # Authentication routes
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout-success/', logout_success, name='logout_success'),
]
