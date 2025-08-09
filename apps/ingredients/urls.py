from django.urls import path
from .views import IngredientListView, IngredientDetailView

app_name = 'ingredients'

urlpatterns = [
    path('list/', IngredientListView.as_view(), name='list'),
    path('detail/<int:pk>/', IngredientDetailView.as_view(), name='detail'),
]
