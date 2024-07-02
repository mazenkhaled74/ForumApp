from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_manager.urls')),
    path('content/', include('content.urls')),
    path('moderation/', include('moderation.urls')),
]
