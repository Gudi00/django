# notifications/admin.py
from django.contrib import admin
from notifications.models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_subscribed')
    list_filter = ('is_subscribed',)
    search_fields = ('user__username', 'user__email')