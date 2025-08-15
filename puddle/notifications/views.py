# notifications/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

def unsubscribe(request, user_id):
    try:
        user = User.objects.get(id=user_id, is_active=True)
        user.is_active = False  # Или добавьте поле is_subscribed в модель User
        user.save()
        return HttpResponse("Вы успешно отписаны от рассылок.")
    except User.DoesNotExist:
        return HttpResponse("Пользователь не найден.", status=404)