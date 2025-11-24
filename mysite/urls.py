from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('login')),   # root -> login

    # keep accounts routes
    path('', include('accounts.urls')),

    # *** ADD THIS LINE to register the dailyreports named URLs (psp, etc.) ***
    path('', include('dailyreports.urls')),

    # existing API include
    path('api/', include('dailyreports.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
