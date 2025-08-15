from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import os
from orders.models import Order
from carts.models import Cart
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from reportlab.lib.pagesizes import letter  # Для размера страницы
from reportlab.pdfgen import canvas  # Для генерации PDF
from django.conf import settings  # Для пути сохранения
import os
import django
from django.core.mail import send_mail
# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puddle.settings')

# Setup Django
django.setup()

# Now it's safe to import models
from users.models import User
print(User.objects.count())


@shared_task
def send_daily_notifications():
    users = User.objects.all()
    message = "Привет! Сегодня акция на мебель - скидка 20%!"
    
    for user in users:
        if user.email:
            send_mail(
                'Ежедневное уведомление от Puddle',
                message,
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )
    
    return f"Уведомления отправлены {len(users)} пользователям"
    

@shared_task
def cleanup_abandoned_carts():
    """
    Удаляет корзины, старше 1 месяца.
    """
    one_month_ago = timezone.now() - timedelta(days=30)  # 1 месяц ≈ 30 дней; для точности используй dateutil.relativedelta

    abandoned_carts = Cart.objects.filter(created_timestamp__lt=one_month_ago)
    count = abandoned_carts.count()
    abandoned_carts.delete()

    return f"Удалено {count} заброшенных корзин"




  # Импортируй свои модели; адаптируй путь если нужно

@shared_task
def generate_daily_report():
    """
    Создаёт отчёт о количестве товаров, добавленных в корзины и заказанных за последний день.
    Отправляет отчёт по email админу и сохраняет PDF на сервере.
    """
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Количество товаров в корзинах (адаптируй под твои модели)
    carts_today = Cart.objects.filter(created_timestamp__date=today)
    carts_items_count = sum(cart.quantity for cart in carts_today)  # Или aggregate если есть quantity

    # Количество заказанных товаров
    orders_today = Order.objects.filter(created_timestamp__date=today)
    orders_items_count = sum(order.id for order in orders_today)  # Адаптируй под модели

    report_message = f"""
    Ежедневный отчёт за {today}:
    - Товаров добавлено в корзины: {carts_items_count}
    - Товаров заказано: {orders_items_count}
    """

    # Отправка email (как раньше)                                          Отправить на почту
    send_mail(
        'Ежедневный отчёт по мебели',
        report_message,
        'no-reply@yourdomain.com',
        ['admin@yourdomain.com'],  # Укажи email админа
        fail_silently=False,
    )

    # Генерация PDF
    report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')  # Папка для отчётов                               ######Придумать более красивое отображение
    os.makedirs(report_dir, exist_ok=True)  # Создаём папку если нет
    pdf_filename = f'daily_report_{today}.pdf'
    pdf_path = os.path.join(report_dir, pdf_filename)

    # Создаём PDF с помощью reportlab
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter  # Размеры страницы

    # Добавляем заголовок
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, f"Ежедневный отчёт за {today}")

    # Добавляем данные
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"- Товаров добавлено в корзины: {carts_items_count}")
    c.drawString(100, height - 170, f"- Товаров заказано: {orders_items_count}")

    # Сохраняем PDF
    c.save()

    return f"Отчёт отправлен и PDF сохранён: {pdf_path}"


# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mass_mail
from django.template import Template, Context
from users.models import User
from django.conf import settings
from celery.utils.log import get_task_logger
from time import sleep
import math
import logging

logger = get_task_logger(__name__)
BATCH_SIZE = 100
DELAY_BETWEEN_BATCHES = 2

@shared_task(bind=True, rate_limit='10/m', max_retries=3)
def send_batch_emails(self, message_template, subject, batch_user_ids, from_email='no-reply@yourdomain.com'):
    try:
        users = User.objects.filter(id__in=batch_user_ids, is_active=True, email__isnull=False)
        messages = []

        for user in users:
            context = Context({'user': user, 'message': message_template})
            rendered_message = Template(message_template).render(context)
            messages.append((subject, rendered_message, from_email, [user.email]))

        if messages:
            if settings.DEBUG:
                if logger.isEnabledFor(logging.INFO):
                    logger.info(f"DEBUG=True: Симуляция отправки {len(messages)} email:")
                    for msg in messages:
                        logger.info(f"  - {msg[0]} to {msg[3][0]}: {msg[1][:50]}...")
            else:
                send_mass_mail(messages, fail_silently=False)
                if logger.isEnabledFor(logging.ERROR):
                    logger.error(f"Отправлено {len(messages)} email в батче")

        return f"Батч {'симулирован' if settings.DEBUG else 'отправлен'}: {len(users)} пользователей"

    except Exception as exc:
        if logger.isEnabledFor(logging.ERROR):
            logger.error(f"Ошибка в батче: {exc}")
        self.retry(exc=exc, countdown=300)

@shared_task
def send_mass_notifications(message, subject, user_ids=None, batch_size=BATCH_SIZE, delay=DELAY_BETWEEN_BATCHES, dry_run=False):
    if user_ids is None:
        user_ids = list(User.objects.filter(is_active=True, email__isnull=False).values_list('id', flat=True))

    num_users = len(user_ids)

    if settings.DEBUG and logger.isEnabledFor(logging.INFO):
        logger.info(f"DEBUG=True: Запуск симуляции рассылки для {num_users} пользователей")
    elif not settings.DEBUG and logger.isEnabledFor(logging.ERROR):
        logger.error(f"Запуск реальной рассылки для {num_users} пользователей")

    if num_users == 0:
        return "Нет пользователей для отправки"

    if dry_run or settings.DEBUG:
        if logger.isEnabledFor(logging.INFO):
            logger.info(f"Dry-run/DEBUG: Симуляция отправки {num_users} сообщений")
        return f"Dry-run/DEBUG завершён: {num_users} симулировано"

    if num_users <= batch_size:
        send_batch_emails.delay(message, subject, user_ids)
    else:
        num_batches = math.ceil(num_users / batch_size)
        tasks = []
        for i in range(num_batches):
            batch_ids = user_ids[i * batch_size : (i + 1) * batch_size]
            tasks.append(send_batch_emails.s(message, subject, batch_ids))
            if i < num_batches - 1:
                tasks.append(shared_task(lambda: sleep(delay)))

        chain(*tasks).delay()

    return f"Рассылка {'симулирована' if settings.DEBUG else 'запущена'} для {num_users} пользователей"