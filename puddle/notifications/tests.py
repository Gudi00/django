# import logging
# from unittest.mock import patch, Mock, ANY
# from django.test import TestCase, override_settings
# from django.core.mail import get_connection
# from users.models import User
# from goods.models import Products, Categories
# from notifications.tasks import (
#     send_batch_emails, send_mass_notifications, send_daily_discounts,
#     send_daily_notifications, cleanup_abandoned_carts, generate_daily_report
# )
# from notifications.models import Subscription
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
# from django.utils import timezone
# from datetime import timedelta
# from carts.models import Cart
# from orders.models import Order
# import pytest
# from reportlab.lib.pagesizes import letter


# # Настройка логгера для тестов
# logger = logging.getLogger('notifications.tasks')
# settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem'
# self.outbox = get_connection().get_outbox()
# @pytest.mark.django_db
# class NotificationTasksTests(TestCase):
#     def setUp(self):
#         """Создание тестовых данных и настройка окружения."""
#         # Исправляем EMAIL_BACKEND на правильный путь
#         settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem'
#         self.outbox = get_connection().get_outbox()
#         self.locmem.clear()

#         # Создаём категорию
#         self.category = Categories.objects.create(
#             name='Мебель',
#             slug='furniture'
#         )

#         # Создаём товары
#         self.product1 = Products.objects.create(
#             name='Тестовый диван',
#             slug='test-sofa',
#             description='Удобный диван со скидкой',
#             price=10000.00,
#             discount=20.00,
#             quantity=10,
#             category=self.category
#         )
#         self.product2 = Products.objects.create(
#             name='Тестовый стол',
#             slug='test-table',
#             description='Стол без скидки',
#             price=5000.00,
#             discount=0.00,
#             quantity=5,
#             category=self.category
#         )

#         # Создаём пользователей и подписки
#         self.user1 = User.objects.create_user(
#             username='user1',
#             email='user1@example.com',
#             first_name='Иван',
#             is_active=True
#         )
#         Subscription.objects.create(user=self.user1, is_subscribed=True)

#         self.user2 = User.objects.create_user(
#             username='user2',
#             email='user2@example.com',
#             first_name='Мария',
#             is_active=True
#         )
#         Subscription.objects.create(user=self.user2, is_subscribed=True)

#         self.user3 = User.objects.create_user(
#             username='user3',
#             email='',
#             first_name='Алексей',
#             is_active=True
#         )
#         Subscription.objects.create(user=self.user3, is_subscribed=True)

#         self.user4 = User.objects.create_user(
#             username='user4',
#             email='user4@example.com',
#             first_name='Елена',
#             is_active=False
#         )
#         Subscription.objects.create(user=self.user4, is_subscribed=True)

#         self.user5 = User.objects.create_user(
#             username='user5',
#             email='user5@example.com',
#             first_name='Ольга',
#             is_active=True
#         )
#         Subscription.objects.create(user=self.user5, is_subscribed=False)

#         # Данные для корзин
#         self.old_cart = Cart.objects.create(
#             created_timestamp=timezone.now() - timedelta(days=31),
#             quantity=2
#         )
#         self.new_cart = Cart.objects.create(
#             created_timestamp=timezone.now(),
#             quantity=1
#         )

#         # Данные для заказов
#         self.order = Order.objects.create(
#             created_timestamp=timezone.now()
#         )

#     def test_send_daily_notifications_success(self):
#         """Тест успешной отправки ежедневных уведомлений."""
#         with override_settings(DEBUG=False):
#             result = send_daily_notifications.delay().get()

#             self.assertEqual(result, "Уведомления отправлены 2 пользователям")
#             self.assertEqual(len(self.outbox), 2)
#             self.assertEqual(self.outbox[0].subject, 'Ежедневное уведомление от Puddle')
#             self.assertEqual(self.outbox[0].to, ['user1@example.com'])
#             self.assertIn('скидка 20%!', self.outbox[0].body)

#     def test_send_daily_notifications_no_subscribers(self):
#         """Тест отправки уведомлений без подписанных пользователей."""
#         Subscription.objects.filter(is_subscribed=True).update(is_subscribed=False)
#         result = send_daily_notifications.delay().get()

#         self.assertEqual(result, "Нет пользователей для отправки")
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_daily_notifications_debug_mode(self, caplog):
#         """Тест симуляции отправки уведомлений в режиме DEBUG=True."""
#         with override_settings(DEBUG=True):
#             caplog.set_level(logging.INFO)
#             result = send_daily_notifications.delay().get()

#             self.assertEqual(result, "Уведомления симулированы для 2 пользователей")
#             self.assertEqual(len(self.outbox), 0)
#             self.assertIn("DEBUG=True: Симуляция отправки 2 уведомлений", caplog.text)

#     def test_cleanup_abandoned_carts_success(self):
#         """Тест успешной очистки заброшенных корзин."""
#         result = cleanup_abandoned_carts.delay().get()

#         self.assertEqual(result, "Удалено 1 заброшенных корзин")
#         self.assertFalse(Cart.objects.filter(id=self.old_cart.id).exists())
#         self.assertTrue(Cart.objects.filter(id=self.new_cart.id).exists())

#     def test_cleanup_abandoned_carts_no_carts(self):
#         """Тест очистки корзин, когда нет заброшенных."""
#         Cart.objects.filter(created_timestamp__lt=timezone.now() - timedelta(days=30)).delete()
#         result = cleanup_abandoned_carts.delay().get()

#         self.assertEqual(result, "Нет заброшенных корзин")
#         self.assertEqual(Cart.objects.count(), 1)

#     @patch('reportlab.pdfgen.canvas.Canvas')
#     @patch('os.makedirs')
#     @patch('django.conf.settings.MEDIA_ROOT', '/tmp/media')
#     def test_generate_daily_report_success(self, mock_makedirs, mock_canvas):
#         """Тест успешной генерации и отправки отчёта."""
#         mock_c = Mock()
#         mock_canvas.return_value = mock_c

#         result = generate_daily_report.delay().get()

#         self.assertIn("Отчёт отправлен и PDF сохранён", result)
#         self.assertEqual(len(self.outbox), 1)
#         self.assertEqual(self.outbox[0].subject, 'Ежедневный отчёт по мебели')
#         self.assertIn('Товаров добавлено в корзины: 1', self.outbox[0].body)
#         self.assertIn('Заказов создано: 1', self.outbox[0].body)
#         mock_c.drawString.assert_any_call(100, letter[1] - 100, ANY)
#         mock_c.save.assert_called_once()

#     def test_generate_daily_report_debug_mode(self, caplog):
#         """Тест симуляции отправки отчёта в режиме DEBUG=True."""
#         with override_settings(DEBUG=True):
#             caplog.set_level(logging.INFO)
#             result = generate_daily_report.delay().get()

#             self.assertIn("Отчёт отправлен и PDF сохранён", result)
#             self.assertEqual(len(self.outbox), 0)
#             self.assertIn("DEBUG=True: Симуляция отправки отчёта", caplog.text)

#     def test_send_batch_emails_success(self):
#         """Тест успешной отправки батча писем."""
#         with override_settings(DEBUG=False):
#             message_template = 'Привет, {{ user.first_name }}! {{ message }}'
#             subject = 'Тестовое письмо'
#             user_ids = [self.user1.id, self.user2.id]

#             result = send_batch_emails.delay(message_template, subject, user_ids).get()

#             self.assertEqual(result, 'Батч отправлен: 2 пользователей')
#             self.assertEqual(len(self.outbox), 2)
#             self.assertEqual(self.outbox[0].subject, 'Тестовое письмо')
#             self.assertEqual(self.outbox[0].to, ['user1@example.com'])
#             self.assertEqual(self.outbox[1].to, ['user2@example.com'])
#             self.assertIn('Привет, Иван!', self.outbox[0].body)
#             self.assertIn('Привет, Мария!', self.outbox[1].body)

#     def test_send_batch_emails_no_subscribers(self):
#         """Тест отправки батча без подписанных пользователей."""
#         Subscription.objects.filter(is_subscribed=True).update(is_subscribed=False)
#         message_template = 'Привет, {{ user.first_name }}! {{ message }}'
#         subject = 'Тестовое письмо'
#         user_ids = [self.user1.id, self.user2.id]

#         result = send_batch_emails.delay(message_template, subject, user_ids).get()
#         self.assertEqual(result, 'Батч отправлен: 0 пользователей')
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_batch_emails_debug_mode(self, caplog):
#         """Тест симуляции отправки в режиме DEBUG=True."""
#         with override_settings(DEBUG=True):
#             caplog.set_level(logging.INFO)
#             message_template = 'Привет, {{ user.first_name }}! {{ message }}'
#             subject = 'Тестовое письмо'
#             user_ids = [self.user1.id, self.user2.id]

#             result = send_batch_emails.delay(message_template, subject, user_ids).get()

#             self.assertEqual(result, 'Батч симулирован: 2 пользователей')
#             self.assertEqual(len(self.outbox), 0)
#             self.assertIn('DEBUG=True: Симуляция отправки 2 email', caplog.text)
#             self.assertIn('Привет, Иван!', caplog.text)
#             self.assertIn('Привет, Мария!', caplog.text)

#     def test_send_batch_emails_empty_users(self):
#         """Тест отправки батча с пустым списком пользователей."""
#         result = send_batch_emails.delay('Test', 'Subject', []).get()
#         self.assertEqual(result, 'Батч отправлен: 0 пользователей')
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_batch_emails_smtp_error(self, caplog):
#         """Тест обработки ошибки SMTP."""
#         with override_settings(DEBUG=False):
#             with patch('django.core.mail.send_mass_mail', side_effect=Exception('SMTP Error')):
#                 caplog.set_level(logging.ERROR)
#                 user_ids = [self.user1.id]
#                 task = send_batch_emails.delay('Test', 'Subject', user_ids)
#                 with self.assertRaises(Exception):
#                     task.get()

#                 self.assertIn('Ошибка в send_batch_emails: SMTP Error', caplog.text)

#     def test_send_mass_notifications_single_batch(self):
#         """Тест отправки массовых уведомлений в одном батче."""
#         with override_settings(DEBUG=False):
#             message = 'Привет, {{ user.first_name }}! Тест.'
#             subject = 'Массовое уведомление'
#             user_ids = [self.user1.id, self.user2.id]

#             result = send_mass_notifications.delay(message, subject, user_ids).get()

#             self.assertEqual(result, 'Рассылка запущена для 2 пользователей')
#             self.assertEqual(len(self.outbox), 2)
#             self.assertEqual(self.outbox[0].to, ['user1@example.com'])
#             self.assertEqual(self.outbox[1].to, ['user2@example.com'])

#     @patch('notifications.tasks.chain')
#     def test_send_mass_notifications_multiple_batches(self, mock_chain):
#         """Тест отправки массовых уведомлений с несколькими батчами."""
#         with override_settings(DEBUG=False):
#             for i in range(101):
#                 user = User.objects.create_user(
#                     username=f'test{i}',
#                     email=f'test{i}@example.com',
#                     is_active=True
#                 )
#                 Subscription.objects.create(user=user, is_subscribed=True)

#             result = send_mass_notifications.delay('Test', 'Subject').get()
#             self.assertEqual(result, 'Рассылка запущена для 104 пользователей')
#             mock_chain.assert_called()

#     def test_send_mass_notifications_no_subscribers(self):
#         """Тест отправки массовых уведомлений без подписанных пользователей."""
#         Subscription.objects.filter(is_subscribed=True).update(is_subscribed=False)
#         result = send_mass_notifications.delay('Test', 'Subject').get()
#         self.assertEqual(result, 'Нет пользователей для отправки')
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_mass_notifications_dry_run(self, caplog):
#         """Тест dry-run режима массовых уведомлений."""
#         caplog.set_level(logging.INFO)
#         result = send_mass_notifications.delay('Test', 'Subject', None, 100, 2, True).get()
#         self.assertEqual(result, 'Dry-run/DEBUG завершён: 2 симулировано')
#         self.assertEqual(len(self.outbox), 0)
#         self.assertIn('Dry-run/DEBUG: Симуляция отправки 2 сообщений', caplog.text)

#     def test_send_daily_discounts_success(self):
#         """Тест успешной отправки скидок."""
#         with override_settings(DEBUG=False, BASE_URL='http://localhost:8000'):
#             result = send_daily_discounts.delay().get()

#             self.assertEqual(result, 'Рассылка скидок завершена для 2 пользователей')
#             self.assertEqual(len(self.outbox), 2)
#             self.assertEqual(self.outbox[0].subject, 'Ежедневные скидки на мебель')
#             self.assertEqual(self.outbox[0].to, ['user1@example.com'])
#             self.assertIn('Тестовый диван', self.outbox[0].alternatives[0][0])
#             self.assertIn('http://localhost:8000/catalog/product/test-sofa/', self.outbox[0].alternatives[0][0])
#             self.assertIn('Отписаться', self.outbox[0].alternatives[0][0])

#     def test_send_daily_discounts_no_discounts(self, caplog):
#         """Тест отправки скидок без товаров со скидкой."""
#         Products.objects.filter(discount__gt=0).update(discount=0)
#         caplog.set_level(logging.INFO)
#         result = send_daily_discounts.delay().get()

#         self.assertEqual(result, 'Нет товаров со скидками для рассылки')
#         self.assertEqual(len(self.outbox), 0)
#         self.assertIn('Нет товаров со скидками для рассылки', caplog.text)

#     def test_send_daily_discounts_no_subscribers(self):
#         """Тест отправки скидок без подписанных пользователей."""
#         Subscription.objects.filter(is_subscribed=True).update(is_subscribed=False)
#         result = send_daily_discounts.delay().get()
#         self.assertEqual(result, 'Рассылка скидок завершена для 0 пользователей')
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_daily_discounts_debug_mode(self, caplog):
#         """Тест симуляции отправки скидок в режиме DEBUG=True."""
#         with override_settings(DEBUG=True):
#             caplog.set_level(logging.INFO)
#             result = send_daily_discounts.delay().get()

#             self.assertEqual(result, 'Рассылка скидок симулирована для 2 пользователей')
#             self.assertEqual(len(self.outbox), 0)
#             self.assertIn('DEBUG=True: Симуляция отправки 2 писем', caplog.text)
#             self.assertIn('user1@example.com', caplog.text)
#             self.assertIn('user2@example.com', caplog.text)

#     def test_send_daily_discounts_smtp_error(self, caplog):
#         """Тест обработки ошибки SMTP в send_daily_discounts."""
#         with override_settings(DEBUG=False):
#             with patch('django.core.mail.get_connection', side_effect=Exception('SMTP Error')):
#                 caplog.set_level(logging.ERROR)
#                 task = send_daily_discounts.delay()
#                 with self.assertRaises(Exception):
#                     task.get()

#                 self.assertIn('Ошибка в send_daily_discounts: SMTP Error', caplog.text)

# # notifications/tests.py
# import logging
# from unittest.mock import patch
# from django.test import TestCase, override_settings
# from django.core.mail import get_connection
# from django.contrib.auth.models import User, Group, Permission
# from goods.models import Products, Categories
# from notifications.tasks import send_daily_discounts
# from notifications.models import Subscription
# from django.conf import settings
# from django.utils import timezone
# from datetime import timedelta
# import pytest

# logger = logging.getLogger('notifications.tasks')

# @pytest.mark.django_db
# class NotificationTasksTests(TestCase):
#     def setUp(self):
#         """Set up test data and environment."""
#         settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
#         self.connection = get_connection()
#         self.outbox = self.connection.get_outbox()
#         self.outbox.clear()

#         # Create groups and permissions
#         client_group = Group.objects.create(name='Client')
#         manager_group = Group.objects.create(name='Manager')
#         content_editor_group = Group.objects.create(name='ContentEditor')
#         admin_group = Group.objects.create(name='Administrator')
#         support_group = Group.objects.create(name='Support')

#         # Assign permissions (simplified for testing)
#         product_ct = ContentType.objects.get_for_model(Products)
#         client_group.permissions.add(
#             Permission.objects.get(content_type=product_ct, codename='view_product')
#         )
#         manager_group.permissions.add(
#             Permission.objects.get(content_type=product_ct, codename='add_product'),
#             Permission.objects.get(content_type=product_ct, codename='change_product')
#         )
#         content_editor_group.permissions.add(
#             Permission.objects.get(content_type=product_ct, codename='change_product')
#         )
#         admin_group.permissions.set(Permission.objects.all())
#         support_group.permissions.add(
#             Permission.objects.get(content_type=Order, codename='view_order')
#         )

#         # Create category
#         self.category = Categories.objects.create(name='Furniture', slug='furniture')

#         # Create products
#         self.product1 = Products.objects.create(
#             name='Test Sofa',
#             slug='test-sofa',
#             description='Comfortable sofa with discount',
#             price=1000.00,
#             discount=20.00,
#             quantity=10,
#             category=self.category
#         )

#         # Create users and subscriptions
#         self.user1 = User.objects.create_user(
#             username='user1', email='user1@example.com', first_name='John', is_active=True
#         )
#         Subscription.objects.create(user=self.user1, is_subscribed=True)
#         self.user1.groups.add(client_group)

#         self.user2 = User.objects.create_user(
#             username='manager1', email='manager1@example.com', first_name='Jane', is_active=True
#         )
#         Subscription.objects.create(user=self.user2, is_subscribed=True)
#         self.user2.groups.add(manager_group)

#     def test_send_daily_discounts_success(self):
#         """Test successful sending of daily discount emails."""
#         with override_settings(DEBUG=False, BASE_URL='http://localhost:8000'):
#             result = send_daily_discounts.delay().get()

#             self.assertEqual(result, 'Sent discount emails to 2 users')
#             self.assertEqual(len(self.outbox), 2)
#             self.assertEqual(self.outbox[0].subject, 'Daily Discounts on Furniture')
#             self.assertEqual(self.outbox[0].to, ['user1@example.com'])
#             self.assertIn('Test Sofa', self.outbox[0].alternatives[0][0])
#             self.assertIn('http://localhost:8000/catalog/product/test-sofa/', self.outbox[0].alternatives[0][0])

#     def test_send_daily_discounts_no_subscribers(self):
#         """Test sending discounts with no subscribed users."""
#         Subscription.objects.filter(is_subscribed=True).update(is_subscribed=False)
#         result = send_daily_discounts.delay().get()

#         self.assertEqual(result, 'No subscribed users')
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_daily_discounts_no_discounts(self):
#         """Test sending discounts with no discounted products."""
#         Products.objects.filter(discount__gt=0).update(discount=0)
#         result = send_daily_discounts.delay().get()

#         self.assertEqual(result, 'No discounted products available')
#         self.assertEqual(len(self.outbox), 0)

#     def test_send_daily_discounts_debug_mode(self):
#         """Test simulating discount emails in DEBUG mode."""
#         with override_settings(DEBUG=True):
#             with self.assertLogs('notifications.tasks', level='INFO') as cm:
#                 result = send_daily_discounts.delay().get()

#                 self.assertEqual(result, 'Simulated sending to 2 users')
#                 self.assertEqual(len(self.outbox), 0)
#                 self.assertIn('DEBUG=True: Simulating sending 2 discount emails', cm.output[0])

#     def test_group_permissions(self):
#         """Test group permissions for different roles."""
#         client = self.user1
#         manager = self.user2

#         # Client permissions
#         self.assertTrue(client.has_perm('goods.view_product'))
#         self.assertFalse(client.has_perm('goods.change_product'))
#         self.assertTrue(client.has_perm('orders.add_order'))
#         self.assertTrue(client.has_perm('carts.add_cart'))

#         # Manager permissions
#         self.assertTrue(manager.has_perm('goods.add_product'))
#         self.assertTrue(manager.has_perm('goods.change_product'))
#         self.assertFalse(manager.has_perm('auth.delete_user'))







# def test_send_order_confirmation(self):
#     order = Order.objects.create(
#         user=self.user1,
#         phone_number='1234567890',
#         created_timestamp=timezone.now()
#     )
#     OrderItem.objects.create(
#         order=order,
#         product=self.product1,
#         name=self.product1.name,
#         price=self.product1.sell_price(),
#         quantity=1
#     )
#     with override_settings(DEBUG=False):
#         result = send_order_confirmation.delay(order.id, self.user1.id).get()
#         self.assertEqual(result, f"Письмо отправлено для заказа {order.id}")
#         self.assertEqual(len(self.outbox), 1)
#         self.assertEqual(self.outbox[0].subject, f'Подтверждение заказа #{order.id}')
#         self.assertIn(f'Детали заказа #{order.id}', self.outbox[0].alternatives[0][0])