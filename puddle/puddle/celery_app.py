# puddle/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puddle.settings')  # Укажи правильный путь к settings

app = Celery('puddle')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['notifications'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')