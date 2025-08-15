# notifications/urls.py
from django.urls import path
from .views import unsubscribe

urlpatterns = [
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
]