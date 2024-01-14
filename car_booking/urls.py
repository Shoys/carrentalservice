from django.contrib import admin, auth
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.apiurls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('booking.urls')),
]
