from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.recipes.views import welcome, login_view, logout_view, logout_success

urlpatterns = [
    path("admin/", admin.site.urls),

    # Namespaced includes
    path("recipes/", include(("apps.recipes.urls", "recipes"), namespace="recipes")),
    path("ingredients/", include(("apps.ingredients.urls", "ingredients"), namespace="ingredients")),
    path("sales/", include(("apps.sales.urls", "sales"), namespace="sales")),

    # Auth at project level (single source of truth)
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("logout-success/", logout_success, name="logout_success"),

    # Root
    path("", welcome, name="welcome_root"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
