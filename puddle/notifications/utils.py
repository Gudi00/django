# # notifications/utils.py
# from celery import shared_task, chain
# from django.core.mail import send_mass_mail
# from django.template import Template, Context
# from users.models import User
# from django.conf import settings
# from celery.utils.log import get_task_logger
# from time import sleep
# import math
# import logging

# logger = get_task_logger(__name__)
# BATCH_SIZE = 100
# DELAY_BETWEEN_BATCHES = 2

# @shared_task(bind=True, rate_limit='10/m', max_retries=3)
# def send_batch_emails(self, message_template, subject, batch_user_ids, from_email='no-reply@yourdomain.com'):
#     try:
#         users = User.objects.filter(id__in=batch_user_ids, is_active=True, email__isnull=False)
#         messages = []

#         for user in users:
#             context = Context({'user': user, 'message': message_template})
#             rendered_message = Template(message_template).render(context)
#             messages.append((subject, rendered_message, from_email, [user.email]))

#         if messages:
#             if settings.DEBUG:
#                 if logger.isEnabledFor(logging.INFO):
#                     logger.info(f"DEBUG=True: Симуляция отправки {len(messages)} email:")
#                     for msg in messages:
#                         logger.info(f"  - {msg[0]} to {msg[3][0]}: {msg[1][:50]}...")
#             else:
#                 send_mass_mail(messages, fail_silently=False)
#                 if logger.isEnabledFor(logging.ERROR):
#                     logger.error(f"Отправлено {len(messages)} email в батче")

#         return f"Батч {'симулирован' if settings.DEBUG else 'отправлен'}: {len(users)} пользователей"

#     except Exception as exc:
#         if logger.isEnabledFor(logging.ERROR):
#             logger.error(f"Ошибка в батче: {exc}")
#         self.retry(exc=exc, countdown=300)

# @shared_task
# def send_mass_notifications(message, subject, user_ids=None, batch_size=BATCH_SIZE, delay=DELAY_BETWEEN_BATCHES, dry_run=False):
#     """
#     Запускает массовую рассылку email. Принимает список user_ids вместо QuerySet.
#     """
#     if user_ids is None:
#         user_ids = list(User.objects.filter(is_active=True, email__isnull=False).values_list('id', flat=True))

#     num_users = len(user_ids)

#     if settings.DEBUG and logger.isEnabledFor(logging.INFO):
#         logger.info(f"DEBUG=True: Запуск симуляции рассылки для {num_users} пользователей")
#     elif not settings.DEBUG and logger.isEnabledFor(logging.ERROR):
#         logger.error(f"Запуск реальной рассылки для {num_users} пользователей")

#     if num_users == 0:
#         return "Нет пользователей для отправки"

#     if dry_run or settings.DEBUG:
#         if logger.isEnabledFor(logging.INFO):
#             logger.info(f"Dry-run/DEBUG: Симуляция отправки {num_users} сообщений")
#         return f"Dry-run/DEBUG завершён: {num_users} симулировано"

#     if num_users <= batch_size:
#         send_batch_emails.delay(message, subject, user_ids)
#     else:
#         num_batches = math.ceil(num_users / batch_size)
#         tasks = []
#         for i in range(num_batches):
#             batch_ids = user_ids[i * batch_size : (i + 1) * batch_size]
#             tasks.append(send_batch_emails.s(message, subject, batch_ids))
#             if i < num_batches - 1:
#                 tasks.append(shared_task(lambda: sleep(delay)))

#         chain(*tasks).delay()

#     return f"Рассылка {'симулирована' if settings.DEBUG else 'запущена'} для {num_users} пользователей"