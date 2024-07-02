from django.urls import path
from auth_manager.views import RegisterView,LogInView, GetReputationAPIView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LogInView.as_view(), name='login'),
    path('reputation/<int:pk>', GetReputationAPIView.as_view(), name='get_reputation'),
    
]