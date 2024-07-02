from django.contrib import admin
from .models import CustomUser, Badge
admin.site.register(CustomUser)
admin.site.register(Badge)
