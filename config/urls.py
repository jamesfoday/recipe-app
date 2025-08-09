from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from apps.recipes.views import welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('apps.recipes.urls')),
        
      path('ingredients/', include('apps.ingredients.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
