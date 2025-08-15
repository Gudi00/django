# core/models.py
from django.db import models
from users.models import User

class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed'), ('simulated', 'Simulated')])