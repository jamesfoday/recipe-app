from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from apps.recipes.views import welcome
from apps.recipes.views import login_view, logout_view, logout_success


urlpatterns = [
    path('admin/', admin.site.urls),
    
   path('recipes/', include('apps.recipes.urls')),
        
    path('ingredients/', include('apps.ingredients.urls')),
     path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout-success/', logout_success, name='logout_success'),
    path('sales/', include(('apps.sales.urls', 'sales'), namespace='sales')),
     path('', welcome, name='welcome_root'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
