# Puddle — Furniture Store

> Полнофункциональная платформа интернет-магазина мебели с REST API, асинхронными задачами и двухуровневой системой администрирования.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)
![Last Commit](https://img.shields.io/github/last-commit/Gudi00/django)
![Stars](https://img.shields.io/github/stars/Gudi00/django?style=social)

---

## 📖 Описание

**Puddle** — это production-ready платформа интернет-магазина мебели, построенная на Django 5.2 и Django REST Framework. Проект реализует полный цикл электронной коммерции: каталог товаров с категориями и скидками, корзину покупок (включая анонимных пользователей), оформление заказов с доставкой, а также систему email-уведомлений с асинхронной обработкой через Celery. Платформа включает две независимые панели администрирования для контент-редакторов и операционной поддержки, развёртывается через Docker Compose и документируется через Swagger / ReDoc.

---

## 💡 Как появилась идея

> 📝 TODO: опиши, что тебя побудило создать именно этот проект — возможно, опыт работы с реальным магазином, учебный курс или желание собрать полноценное портфолио с production-стеком.

---

## 🛠 Технологический стек

### Основные технологии

| Технология | Версия | Для чего используется |
|---|---|---|
| Python | 3.12 | Основной язык разработки |
| Django | 5.2.4 | Web-фреймворк, ORM, аутентификация |
| Django REST Framework | 3.15.2 | REST API, сериализаторы, ViewSets |
| PostgreSQL | 16 | Основная реляционная база данных |
| Redis | 7 | Брокер сообщений для Celery, кэширование |
| Celery | 5.5.3 | Очередь асинхронных задач |
| django-celery-beat | 2.8.1 | Периодические задачи (cron) |
| Flower | 2.0.1 | Мониторинг очереди Celery |
| Gunicorn | 23.0.0 | WSGI-сервер для production |
| Docker / Docker Compose | — | Контейнеризация и оркестрация сервисов |
| drf-spectacular | 0.27.2 | Генерация OpenAPI 3.0 схемы, Swagger UI |
| Pillow | 11.3.0 | Обработка и хранение изображений |
| WhiteNoise | 6.7.0 | Раздача статических файлов |
| django-cors-headers | 4.6.0 | CORS-заголовки для API |
| django-filter | 24.3 | Фильтрация QuerySet через URL-параметры |
| python-decouple | 3.8 | Управление переменными окружения |
| pytest / pytest-django | 8.4.1 / 4.11.1 | Тестирование |
| coverage | 7.10.3 | Покрытие кода тестами |

### Нестандартные и интересные библиотеки

| Библиотека | Версия | Чем интересна |
|---|---|---|
| **ReportLab** | 4.4.3 | Генерация PDF прямо в Django — можно формировать накладные или отчёты на лету |
| **prometheus_client** | 0.22.1 | Метрики в формате Prometheus для интеграции с Grafana/Alertmanager |
| **humanize** | 4.12.3 | Превращает числа и даты в читаемый текст («3 часа назад», «1 234 руб.») |
| **python-crontab** | 3.3.0 | Парсинг и валидация cron-выражений |
| **drf-spectacular** | 0.27.2 | Автогенерация OpenAPI-схемы из кода без ручного написания YAML |

---

## ✨ Возможности

- **Каталог товаров** — продукты по категориям, уникальные slug-URL, система скидок (%)
- **Корзина покупок** — поддержка авторизованных и анонимных пользователей через session_key
- **Оформление заказов** — выбор доставки, адрес, оплата при получении; транзакционное списание остатков
- **Email-уведомления** — подтверждение заказа, ежедневные дайджесты скидок, напоминания о брошенной корзине
- **REST API** — полный CRUD с фильтрацией, поиском, пагинацией и документацией (Swagger / ReDoc)
- **Двойная панель администрирования** — Staff Admin для контент-редакторов и Ops Admin для операционной поддержки
- **Асинхронные задачи** — 5 Celery-задач по расписанию: рассылки, очистка корзин, напоминания
- **Пакетная отправка писем** — батчи по 100 пользователей с rate-limiting и retry с экспоненциальной задержкой
- **Верификация email** — токен с TTL 7 дней; проверка обязательна перед оформлением заказа (настраивается)
- **Управление остатками** — автоматическое уменьшение quantity при создании заказа
- **Мониторинг** — Flower UI для Celery, health-check эндпоинт в Admin, Prometheus-метрики
- **Контейнеризация** — полный docker-compose.yml с PostgreSQL, Redis, Web, Celery Worker, Celery Beat

---

## 🚀 Установка и запуск

### Через Docker Compose (рекомендуется)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Gudi00/django.git
cd django/puddle

# 2. Создать файл с переменными окружения
cp .env.example .env
# Заполнить .env: SECRET_KEY, DB-параметры, EMAIL-реквизиты

# 3. Запустить все сервисы
docker compose up -d --build

# 4. Применить миграции и создать суперпользователя
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Сервисы будут доступны по адресам:

| Сервис | URL |
|---|---|
| Django Web | http://localhost:8000 |
| Staff Admin | http://localhost:8000/staff-admin/ |
| Ops Admin | http://localhost:8000/ops-admin/ |
| Swagger UI | http://localhost:8000/api/docs/ |
| ReDoc | http://localhost:8000/api/redoc/ |
| Flower (Celery) | http://localhost:5555 |

### Локальная установка (без Docker)

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить переменные окружения
cp .env.example .env
# Отредактировать .env

# 4. Применить миграции
python manage.py migrate

# 5. Загрузить тестовые данные (при наличии)
python manage.py loaddata fixtures/*.json

# 6. Запустить сервер разработки
python manage.py runserver

# 7. В отдельных терминалах — Celery Worker и Beat
celery -A puddle worker -l info
celery -A puddle beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Переменные окружения

```env
DEBUG=True
SECRET_KEY=your-secret-key

# База данных
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=puddle_db
SQL_USER=puddle_user
SQL_PASSWORD=your_password
SQL_HOST=localhost
SQL_PORT=5432

# Redis / Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Gmail SMTP
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Верификация email (True/False)
EMAIL_VERIFICATION_REQUIRED=False
```

### Запуск тестов

```bash
# Все тесты с покрытием
pytest --cov=notifications --cov-report=html

# Только конкретное приложение
pytest notifications/tests.py -v
```

---

## 📸 Скриншоты и демо

<!-- SCREENSHOT: Главная страница каталога мебели — сетка товаров с фото, ценами и значками скидок -->
![Каталог товаров](screenshots/screenshot_1.png)

<!-- SCREENSHOT: Страница товара — фото, описание, цена со скидкой, кнопка "Добавить в корзину" -->
![Карточка товара](screenshots/screenshot_2.png)

<!-- SCREENSHOT: Корзина покупок — список товаров, количество, итоговая сумма, кнопка оформления заказа -->
![Корзина](screenshots/screenshot_3.png)

<!-- SCREENSHOT: Swagger UI — список всех API-эндпоинтов с возможностью тестирования прямо в браузере -->
![Swagger API документация](screenshots/screenshot_4.png)

<!-- SCREENSHOT: Staff Admin — интерфейс для контент-редакторов, таблица товаров с поиском и фильтрами -->
![Staff Admin](screenshots/screenshot_5.png)

<!-- SCREENSHOT: Ops Admin — интерфейс операционной поддержки, список заказов с датой и статусом -->
![Ops Admin](screenshots/screenshot_6.png)

<!-- SCREENSHOT: Flower UI — мониторинг очереди Celery, активные воркеры и статус задач -->
![Flower Celery мониторинг](screenshots/screenshot_7.png)

---

## 💼 Как я использую этот проект

> 📝 TODO: опиши, как используешь этот проект в реальной жизни или в рамках учёбы/работы. Например: «Развернул у клиента для небольшого мебельного шоурума» или «Использую как стартовый шаблон для e-commerce проектов».

---

## 👥 Аудитория и пользователи

Проект ориентирован на:

- **Разработчиков**, изучающих production-архитектуру Django-проектов (API + Celery + Docker)
- **Малый и средний бизнес** в сфере торговли мебелью, ищущий готовую основу для интернет-магазина
- **Стартапы**, которым нужна e-commerce платформа с возможностью быстрой кастомизации

> 📝 TODO: укажи реальное количество пользователей/загрузок, если проект уже в production или имеет публичный трафик.

---

## ⚙️ Как реализован проект

### Архитектура

Проект разделён на 6 Django-приложений с чёткими зонами ответственности:

```
puddle/          ← Конфигурация, admin_sites, celery
users/           ← Кастомная модель User, верификация email
goods/           ← Модели Product и Category, API endpoints
carts/           ← Модель Cart, анонимные пользователи
orders/          ← Модели Order / OrderItem, создание заказов
notifications/   ← Celery-задачи, email-шаблоны, логи
```

### Ключевые технические решения

**Двойная панель администрирования**

Вместо одного стандартного `/admin/` реализованы два независимых `AdminSite`:
- `/staff-admin/` — для контент-редакторов (управление товарами, категориями)
- `/ops-admin/` — для операционной поддержки (заказы, пользователи, уведомления)

Каждый сайт имеет собственный дашборд со статистикой, кастомные шаблоны и разграниченные права через группы Django.

**Асинхронные рассылки с батчингом**

Celery Beat запускает 5 периодических задач. Массовые рассылки разбиты на батчи по 100 пользователей с паузами между ними, что предотвращает блокировку SMTP-сервера. Retry-стратегия с экспоненциальной задержкой при ошибках SMTP.

```python
# Пример: батч-рассылка дайджеста скидок
@shared_task(bind=True, max_retries=3)
def send_daily_discounts(self):
    users = User.objects.filter(subscription__is_subscribed=True)
    for batch in chunked(users, 100):
        send_html_email_batch(batch, discounted_products)
        time.sleep(2)  # rate limiting
```

**Транзакционное создание заказа**

Создание заказа оборачивается в `transaction.atomic()`: проверяется наличие товара, декрементируется `quantity`, создаются `OrderItem`, корзина очищается. При любой ошибке транзакция откатывается целиком.

**Кастомный QuerySet для корзины и заказов**

Модели `Cart` и `OrderItem` используют кастомный QuerySet с методами `total_price()` и `total_quantity()`, что позволяет выносить агрегации на уровень ORM и не считать итоги в Python.

**OpenAPI-документация из кода**

`drf-spectacular` автоматически генерирует OpenAPI 3.0 схему из ViewSet-ов, сериализаторов и роутеров — без ручного написания YAML/JSON. Swagger UI доступен по `/api/docs/`.

---

## 🧗 Трудности при разработке

> 📝 TODO: опиши 2-3 сложности, с которыми ты столкнулся при разработке этого проекта. Например: «Настройка batching для Celery без потери писем», «Разделение прав между двумя AdminSite», «Корректная обработка анонимной корзины при авторизации пользователя».

---

## 🔮 Планы развития

> 📝 TODO: опиши как планируешь развивать проект. Возможные направления (замени или дополни своими):
> - Интеграция платёжного шлюза (Stripe / ЮKassa)
> - Frontend на React или Next.js с потреблением REST API
> - WebSocket-уведомления о статусе заказа в реальном времени
> - Экспорт заказов в PDF через ReportLab (библиотека уже подключена)
> - Полноценный дашборд аналитики с Prometheus + Grafana

---

## 📄 Лицензия

Распространяется под лицензией [MIT](LICENSE).

Copyright (c) 2024 Gudi00
