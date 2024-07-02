from django.urls import path
from moderation.views import BlockUserAPIView, UnblockUserAPIView
urlpatterns = [
    path('block/<int:pk>', BlockUserAPIView.as_view()),
    path('unblock/<int:pk>', UnblockUserAPIView.as_view()),
]
