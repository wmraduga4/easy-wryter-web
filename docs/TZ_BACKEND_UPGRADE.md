# ТЕХНИЧЕСКОЕ ЗАДАНИЕ: Easy Writer Backend (Доработка)

**Версия:** 2.0  
**Дата:** Декабрь 2024  
**Базовый проект:** ai-article-backend (существующий)  
**Репозиторий:** easy-writer-backend  
**Разработчик:** Middle+ / Senior-  
**Инструмент:** Cursor AI

---

## СОДЕРЖАНИЕ

1. [Текущее состояние](#1-текущее-состояние)
2. [Этап 1: Регистрация пользователей](#этап-1-регистрация-пользователей)
3. [Этап 2: OAuth интеграция](#этап-2-oauth-интеграция)
4. [Этап 3: Табы и инструменты](#этап-3-табы-и-инструменты)
5. [Этап 4: Новые AI провайдеры](#этап-4-новые-ai-провайдеры)
6. [Этап 5: Генерация изображений](#этап-5-генерация-изображений)
7. [Этап 6: Платёжные системы](#этап-6-платёжные-системы)
8. [Этап 7: Балансы и тарифы](#этап-7-балансы-и-тарифы)
9. [Этап 8: WebSocket](#этап-8-websocket)
10. [Этап 9: Финальное тестирование](#этап-9-финальное-тестирование)

---

## 1. ТЕКУЩЕЕ СОСТОЯНИЕ

### 1.1 Что уже реализовано

| Компонент | Статус |
|-----------|--------|
| FastAPI структура | ✅ |
| PostgreSQL + SQLAlchemy | ✅ |
| Redis + Celery | ✅ (не используется) |
| Модели: Site, Session, Article | ✅ |
| Auth по X-Access-Password | ✅ |
| OpenAI интеграция | ✅ |
| Генерация статей (WordPress) | ✅ |
| SQLAdmin | ✅ |
| Docker инфраструктура | ✅ |

### 1.2 Что нужно добавить

| Компонент | Статус |
|-----------|--------|
| Модель User (пользователи сайта) | ❌ |
| JWT аутентификация | ❌ |
| OAuth (Google, Yandex) | ❌ |
| Табы и инструменты | ❌ |
| GigaChat, YandexGPT | ❌ |
| Kandinsky (изображения) | ❌ |
| Платёжные системы | ❌ |
| Балансы, транзакции | ❌ |
| WebSocket | ❌ |

### 1.3 Архитектура после доработки

```
/api/v1/
├── auth/           # JWT + OAuth (НОВОЕ)
│   ├── register
│   ├── login
│   ├── refresh
│   ├── logout
│   ├── google
│   └── yandex
├── user/           # Профиль, баланс (НОВОЕ)
│   ├── profile
│   ├── balance
│   └── transactions
├── tools/          # Табы и инструменты (НОВОЕ)
│   ├── tabs
│   └── {tool_id}/execute
├── generation/     # Сессии генерации (НОВОЕ)
│   └── sessions
├── images/         # Изображения (НОВОЕ)
│   ├── generate
│   └── upscale
├── payments/       # Платежи (НОВОЕ)
│   ├── create
│   ├── methods
│   └── webhook
├── article/        # Существующее (WordPress)
└── statistics/     # Существующее
```

---

## ЭТАП 1: РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ

**Длительность:** 6 часов

### 1.1 Задачи

- [ ] Создать модель User
- [ ] Миграция БД
- [ ] JWT аутентификация
- [ ] Эндпоинты: register, login, refresh, logout, me
- [ ] Обновить SQLAdmin

### 1.2 Модель User

```python
class User(Base):
    __tablename__ = "users"
    
    id: UUID (PK)
    email: String(255), unique, index
    hashed_password: String(255), nullable  # null для OAuth
    name: String(100), nullable
    provider: Enum('local', 'google', 'yandex'), default='local'
    provider_id: String(255), nullable  # ID в OAuth провайдере
    balance: Integer, default=0  # Райты
    is_active: Boolean, default=True
    is_verified: Boolean, default=False
    created_at: DateTime
    updated_at: DateTime
```

### 1.3 Промпт для Cursor AI

```
Добавь регистрацию пользователей в Easy Writer Backend.

Текущее состояние:
- Проект уже работает (FastAPI + SQLAlchemy + PostgreSQL)
- Есть модели Site, Session, Article для WordPress плагина
- Аутентификация по X-Access-Password для плагина

Требования:
1. Модель User (app/db/models/user.py):
   - Поля как в спецификации выше
   - UUID v7 как PK
   - Индексы: email, provider+provider_id

2. Alembic миграция:
   - Создать таблицу users
   - Формат имени: YYYY-MM-DD_add_users_table.py

3. JWT токены (app/core/security.py):
   - python-jose[cryptography]
   - Access token: 15 минут
   - Refresh token: 7 дней, в httpOnly cookie
   - Алгоритм: HS256
   - Payload: {sub: user_id, exp: timestamp}

4. Хеширование паролей:
   - passlib[bcrypt]
   - hash_password(), verify_password()

5. Эндпоинты (app/api/v1/auth.py):
   POST /auth/register — создание пользователя
   POST /auth/login — вход, возврат токенов
   POST /auth/refresh — обновление access token
   POST /auth/logout — удаление refresh cookie
   GET /auth/me — текущий пользователь (protected)

6. Pydantic схемы (app/schemas/auth.py):
   - RegisterRequest: email, password
   - LoginRequest: email, password
   - TokenResponse: access_token, token_type, expires_in
   - UserResponse: id, email, name, provider, balance, created_at

7. Dependency (app/core/dependencies.py):
   - get_current_user() — извлечь user из JWT
   - Выбрасывать 401 если токен невалиден

8. Валидация:
   - email: EmailStr
   - password: min 8 символов
   - Проверка уникальности email

9. Логирование через loguru

10. SQLAdmin:
    - Добавить UserAdmin
    - Скрыть hashed_password

Не добавляй комментарии. Не трогай существующий код WordPress API.
```

### 1.4 Тесты

**Тест 1 (Unit):** Хеширование пароля
```bash
docker exec easy_writer_backend python -c "
from app.core.security import hash_password, verify_password
h = hash_password('test123456')
assert verify_password('test123456', h)
print('OK')
"
```

**Тест 2 (Integration):** Регистрация
```bash
curl -X POST https://api.easy-writer.ru/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123456"}'
```
Ожидание: 201, access_token в ответе

**Тест 3 (Manual):** Проверка в SQLAdmin
```
1. Открыть https://easy-writer.ru/admin
2. Перейти в Users
3. Проверить: пользователь создан
```

### 1.5 Критерии готовности

- [ ] Таблица users создана
- [ ] Регистрация работает
- [ ] Логин возвращает токены
- [ ] Refresh обновляет access token
- [ ] GET /auth/me возвращает пользователя
- [ ] SQLAdmin показывает пользователей

---

## ЭТАП 2: OAUTH ИНТЕГРАЦИЯ

**Длительность:** 5 часов

### 2.1 Задачи

- [ ] OAuth Google
- [ ] OAuth Yandex
- [ ] Связывание с существующим аккаунтом

### 2.2 Промпт для Cursor AI

```
Добавь OAuth авторизацию (Google, Yandex) в Easy Writer Backend.

Требования:
1. Переменные окружения:
   GOOGLE_CLIENT_ID
   GOOGLE_CLIENT_SECRET
   GOOGLE_REDIRECT_URI=https://api.easy-writer.ru/api/v1/auth/google/callback
   YANDEX_CLIENT_ID
   YANDEX_CLIENT_SECRET
   YANDEX_REDIRECT_URI=https://api.easy-writer.ru/api/v1/auth/yandex/callback
   FRONTEND_URL=https://easy-writer.ru

2. Эндпоинты:
   GET /auth/google — редирект на Google OAuth
   GET /auth/google/callback — обработка callback
   GET /auth/yandex — редирект на Yandex OAuth
   GET /auth/yandex/callback — обработка callback

3. Flow:
   a) GET /auth/google → редирект на Google
   b) Пользователь авторизуется
   c) Google редиректит на /auth/google/callback?code=...
   d) Backend обменивает code на access_token
   e) Получает email, name, provider_id из Google
   f) Создаёт User или находит существующего
   g) Генерирует JWT токены
   h) Редирект на FRONTEND_URL/auth/callback?token=...

4. Логика поиска/создания пользователя:
   - Если есть User с таким provider+provider_id → логин
   - Если есть User с таким email (local) → связать OAuth
   - Иначе → создать нового User

5. Библиотека: httpx для запросов к OAuth провайдерам

6. Google OAuth URLs:
   - Auth: https://accounts.google.com/o/oauth2/v2/auth
   - Token: https://oauth2.googleapis.com/token
   - UserInfo: https://www.googleapis.com/oauth2/v2/userinfo
   - Scope: email profile

7. Yandex OAuth URLs:
   - Auth: https://oauth.yandex.ru/authorize
   - Token: https://oauth.yandex.ru/token
   - UserInfo: https://login.yandex.ru/info
   - Scope: login:email login:info

8. Обработка ошибок:
   - OAuth отменён → редирект на FRONTEND_URL/login?error=cancelled
   - Ошибка провайдера → редирект на FRONTEND_URL/login?error=provider_error

Не добавляй комментарии.
```

### 2.3 Тесты

**Тест 1 (Unit):** Генерация OAuth URL
```bash
curl https://api.easy-writer.ru/api/v1/auth/google -v
```
Ожидание: 302 редирект на accounts.google.com

**Тест 2 (Integration):** Полный flow
```
1. Открыть https://api.easy-writer.ru/api/v1/auth/google
2. Авторизоваться в Google
3. Проверить редирект на frontend с токеном
```

**Тест 3 (Manual):** Yandex OAuth
```
1. Повторить для Yandex
```

### 2.4 Критерии готовности

- [ ] Google OAuth работает
- [ ] Yandex OAuth работает
- [ ] Новый пользователь создаётся
- [ ] Существующий пользователь логинится
- [ ] Редирект на frontend с токеном

---

## ЭТАП 3: ТАБЫ И ИНСТРУМЕНТЫ

**Длительность:** 8 часов

### 3.1 Задачи

- [ ] Структура табов и инструментов
- [ ] Хранение промптов в YAML
- [ ] Эндпоинты API
- [ ] Выполнение инструментов

### 3.2 Структура табов

```python
TABS = {
    "everyday": {
        "name": "На каждый день",
        "icon": "sun",
        "tools": ["spell_check", "paraphrase", "simplify", "letter", 
                  "social_post", "resume", "summarize", "translate"]
    },
    "education": {
        "name": "Обучение",
        "icon": "graduation-cap",
        "tools": ["essay", "essay_academic", "report", "abstract",
                  "notes", "retelling", "qa_text"]
    },
    "business": {
        "name": "Бизнес",
        "icon": "briefcase",
        "tools": ["contract_generate", "contract_analyze", 
                  "commercial_offer", "business_letter", 
                  "meeting_notes", "presentation_text"]
    },
    "marketing": {
        "name": "Маркетинг",
        "icon": "megaphone",
        "tools": ["seo_article", "product_description", "email_campaign",
                  "landing_text", "press_release", "slogan", "naming"]
    },
    "special": {
        "name": "Особый случай",
        "icon": "sparkles",
        "tools": ["custom_prompt", "greeting_card", "toast", "speech",
                  "image_generate", "image_upscale"]
    }
}
```

### 3.3 Промпт для Cursor AI

```
Добавь систему табов и инструментов в Easy Writer Backend.

Требования:
1. Структура папок:
   prompts/
   ├── everyday/
   │   ├── spell_check.yaml
   │   ├── paraphrase.yaml
   │   └── ...
   ├── education/
   ├── business/
   ├── marketing/
   └── special/

2. Формат YAML файла промпта:
   name: "Проверка орфографии"
   description: "Проверка и исправление ошибок"
   icon: "check-circle"
   supports_modes: ["quick"]
   recommended_provider: "gigachat"
   estimated_cost: 5  # Райтов
   input_schema:
     type: object
     required: ["text"]
     properties:
       text:
         type: string
         minLength: 1
         maxLength: 10000
         title: "Текст"
   system_prompt: |
     Ты — корректор текста. Исправь орфографические и пунктуационные ошибки.
   user_template: |
     Проверь и исправь ошибки в тексте:
     {text}
   output_format: "text"

3. Сервис ToolService (app/services/tools.py):
   - load_tabs() → список табов
   - load_tools(tab_id) → список инструментов
   - get_tool(tool_id) → инструмент с промптом
   - get_schema(tool_id) → JSON Schema
   - execute(tool_id, input, mode, user) → результат

4. Эндпоинты (app/api/v1/tools.py):
   GET /tools/tabs — список табов
   GET /tools/tabs/{tab_id} — инструменты таба
   GET /tools/{tool_id}/schema — JSON Schema формы
   POST /tools/{tool_id}/execute — выполнение

5. Модель GenerationSession (app/db/models/generation.py):
   id: UUID
   user_id: UUID (FK)
   tool_id: String
   mode: Enum('quick', 'standard')
   status: Enum('pending', 'in_progress', 'completed', 'failed')
   input_data: JSONB
   result: Text
   provider_used: String
   tokens_used: Integer
   cost_raits: Integer  # Списано Райтов
   created_at: DateTime
   completed_at: DateTime

6. Execute логика:
   a) Валидация input по schema
   b) Проверка баланса пользователя
   c) Выбор AI провайдера
   d) Генерация
   e) Списание Райтов
   f) Сохранение сессии
   g) Возврат результата

7. Защита эндпоинтов: require get_current_user

8. Кеширование табов и инструментов: Redis, TTL 1 час

Не добавляй комментарии.
```

### 3.4 Тесты

**Тест 1 (Unit):** Загрузка промптов
```bash
docker exec easy_writer_backend python -c "
from app.services.tools import ToolService
service = ToolService()
tabs = service.load_tabs()
print(f'Tabs: {len(tabs)}')
"
```

**Тест 2 (Integration):** API табов
```bash
curl https://api.easy-writer.ru/api/v1/tools/tabs \
  -H "Authorization: Bearer <token>"
```

**Тест 3 (Manual):** Выполнение инструмента
```bash
curl -X POST https://api.easy-writer.ru/api/v1/tools/spell_check/execute \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "Превет мир"}, "mode": "quick"}'
```

### 3.5 Критерии готовности

- [ ] Все YAML промпты созданы
- [ ] GET /tools/tabs возвращает 5 табов
- [ ] GET /tools/{tab}/tools возвращает инструменты
- [ ] POST /execute генерирует результат
- [ ] Райты списываются
- [ ] Сессия сохраняется

---

## ЭТАП 4: НОВЫЕ AI ПРОВАЙДЕРЫ

**Длительность:** 10 часов

### 4.1 Задачи

- [ ] GigaChat (Сбер)
- [ ] YandexGPT
- [ ] Роутер провайдеров
- [ ] Fallback логика

### 4.2 Промпт для Cursor AI

```
Добавь новые AI провайдеры в Easy Writer Backend.

Текущее состояние:
- Есть OpenAI интеграция (app/services/openai_service.py)

Требования:
1. Базовый класс (app/services/ai/base.py):
   class AIProvider(ABC):
       name: str
       @abstractmethod
       async def generate(self, prompt: str, system: str, **kwargs) -> str
       @abstractmethod
       async def count_tokens(self, text: str) -> int

2. GigaChat (app/services/ai/gigachat.py):
   - OAuth токен: POST https://ngw.devices.sberbank.ru:9443/api/v2/oauth
   - Кеширование токена в Redis (TTL 25 минут)
   - Generate: POST https://gigachat.devices.sberbank.ru/api/v1/chat/completions
   - SSL сертификат: certificates/russian_trusted_root_ca.cer
   - Env: GIGACHAT_API_KEY, GIGACHAT_SCOPE

3. YandexGPT (app/services/ai/yandexgpt.py):
   - Endpoint: https://llm.api.cloud.yandex.net/foundationModels/v1/completion
   - Model: yandexgpt-lite (быстрый) или yandexgpt (качественный)
   - Env: YANDEXGPT_API_KEY, YANDEXGPT_FOLDER_ID
   - IAM токен или API key

4. Обновить OpenAI (app/services/ai/openai.py):
   - Наследовать от AIProvider
   - Модель: gpt-4o
   - Прокси: OPENAI_PROXY_URL

5. Роутер (app/services/ai/router.py):
   class AIRouter:
       def select_provider(self, task_type: str, language: str = "ru") -> AIProvider
   
   Логика выбора:
   - Простые задачи на русском → GigaChat
   - Академические тексты → OpenAI (GPT-4o)
   - SEO/маркетинг → OpenAI
   - По умолчанию → GigaChat
   - При ошибке → fallback на следующего

6. Retry логика:
   - 3 попытки
   - Exponential backoff: 1s, 2s, 4s
   - При исчерпании → следующий провайдер

7. Логирование:
   - Провайдер
   - Время запроса
   - Токены
   - Ошибки

8. Метрики в Redis:
   - provider:{name}:requests — счётчик запросов
   - provider:{name}:errors — счётчик ошибок
   - provider:{name}:latency — время ответа

Не добавляй комментарии.
```

### 4.3 Тесты

**Тест 1 (Unit):** GigaChat токен
```bash
docker exec easy_writer_backend python -c "
import asyncio
from app.services.ai.gigachat import GigaChatProvider
provider = GigaChatProvider()
token = asyncio.run(provider._get_token())
print(f'Token: {token[:20]}...')
"
```

**Тест 2 (Integration):** Генерация через GigaChat
```bash
docker exec easy_writer_backend python -c "
import asyncio
from app.services.ai.gigachat import GigaChatProvider
provider = GigaChatProvider()
result = asyncio.run(provider.generate('Привет!', 'Ты помощник'))
print(result)
"
```

**Тест 3 (Manual):** Роутер
```bash
docker exec easy_writer_backend python -c "
from app.services.ai.router import AIRouter
router = AIRouter()
provider = router.select_provider('spell_check', 'ru')
print(f'Selected: {provider.name}')
"
```

### 4.4 Критерии готовности

- [ ] GigaChat генерирует текст
- [ ] YandexGPT генерирует текст
- [ ] OpenAI работает через прокси
- [ ] Роутер выбирает провайдера
- [ ] Fallback при ошибках
- [ ] Токен GigaChat кешируется

---

## ЭТАП 5: ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЙ

**Длительность:** 6 часов

### 5.1 Задачи

- [ ] Kandinsky (FusionBrain)
- [ ] Апскейл через внешний API
- [ ] Сохранение изображений
- [ ] Эндпоинты API

### 5.2 Промпт для Cursor AI

```
Добавь генерацию изображений в Easy Writer Backend.

Требования:
1. Kandinsky / FusionBrain (app/services/ai/kandinsky.py):
   - Auth: X-Key, X-Secret headers
   - Env: FUSIONBRAIN_API_KEY, FUSIONBRAIN_SECRET_KEY
   - Запуск: POST https://api-key.fusionbrain.ai/key/api/v1/text2image/run
   - Статус: GET https://api-key.fusionbrain.ai/key/api/v1/text2image/status/{uuid}
   - Polling: каждые 3 сек, таймаут 120 сек

2. Форматы и размеры:
   - web: 1024x1024
   - banner: 2048x1024
   - print: 2048x2048
   - messenger: 512x512

3. Модель GeneratedImage (app/db/models/image.py):
   id: UUID
   user_id: UUID (FK)
   prompt: Text
   format: Enum('web', 'banner', 'print', 'messenger')
   width: Integer
   height: Integer
   original_path: String  # путь к файлу
   upscaled_path: String (nullable)
   provider: String = 'kandinsky'
   status: Enum('processing', 'completed', 'failed')
   cost_raits: Integer
   created_at: DateTime

4. Апскейл (app/services/upscale.py):
   - Внешний API: UPSCALE_API_URL, UPSCALE_API_KEY
   - Масштабы: 2x, 4x
   - Для print формата — 4x обязателен

5. Хранение файлов:
   - Папка: /uploads/images/
   - Имя: {user_id}/{uuid}.png
   - Volume в Docker

6. Эндпоинты (app/api/v1/images.py):
   POST /images/generate — запуск генерации
   GET /images/{id} — получение изображения
   POST /images/{id}/upscale — апскейл
   GET /images — список изображений пользователя
   DELETE /images/{id} — удаление

7. Celery таск для генерации (долгая операция):
   - generate_image_task(image_id)
   - WebSocket уведомление при завершении

8. Инструмент greeting_card:
   - Вход: occasion, recipient_name, style
   - Шаг 1: Генерация текста (AI)
   - Шаг 2: Генерация промпта для картинки (AI)
   - Шаг 3: Генерация картинки (Kandinsky)
   - Выход: {text, image_url}

Не добавляй комментарии.
```

### 5.3 Тесты

**Тест 1 (Unit):** Kandinsky клиент
```bash
docker exec easy_writer_backend python -c "
from app.services.ai.kandinsky import KandinskyProvider
provider = KandinskyProvider()
print(f'Provider ready: {provider.name}')
"
```

**Тест 2 (Integration):** Генерация изображения
```bash
curl -X POST https://api.easy-writer.ru/api/v1/images/generate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Красивый закат", "format": "web"}'
```

**Тест 3 (Manual):** Поздравительная открытка
```bash
curl -X POST https://api.easy-writer.ru/api/v1/tools/greeting_card/execute \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"input": {"occasion": "birthday", "recipient_name": "Даниил"}, "mode": "quick"}'
```

### 5.4 Критерии готовности

- [ ] Kandinsky генерирует изображения
- [ ] Все форматы работают
- [ ] Апскейл работает
- [ ] Файлы сохраняются
- [ ] Greeting card создаёт текст + картинку

---

## ЭТАП 6: ПЛАТЁЖНЫЕ СИСТЕМЫ

**Длительность:** 8 часов

### 6.1 Задачи

- [ ] ЮKassa
- [ ] Robokassa
- [ ] CloudPayments
- [ ] Т-Банк
- [ ] Webhook обработка

### 6.2 Модели

```python
class Payment(Base):
    __tablename__ = "payments"
    
    id: UUID
    user_id: UUID (FK)
    amount_rub: Integer  # Сумма в рублях
    amount_raits: Integer  # Сумма в Райтах
    provider: Enum('yookassa', 'robokassa', 'cloudpayments', 'tbank')
    external_id: String  # ID в платёжной системе
    status: Enum('pending', 'completed', 'failed', 'refunded')
    created_at: DateTime
    completed_at: DateTime
```

### 6.3 Промпт для Cursor AI

```
Добавь платёжные системы в Easy Writer Backend.

Требования:
1. Переменные окружения:
   # ЮKassa
   YOOKASSA_SHOP_ID
   YOOKASSA_SECRET_KEY
   # Robokassa
   ROBOKASSA_MERCHANT_LOGIN
   ROBOKASSA_PASSWORD1
   ROBOKASSA_PASSWORD2
   # CloudPayments
   CLOUDPAYMENTS_PUBLIC_ID
   CLOUDPAYMENTS_API_SECRET
   # Т-Банк
   TBANK_TERMINAL_KEY
   TBANK_PASSWORD

2. Модель Payment (как выше)

3. Модель Transaction (история операций):
   id: UUID
   user_id: UUID (FK)
   payment_id: UUID (FK, nullable)
   type: Enum('topup', 'spend')
   amount: Integer  # Райты
   description: String
   created_at: DateTime

4. Курс: 1 рубль = 10 Райтов (в конфиге)

5. Сервис PaymentService (app/services/payments.py):
   - create_payment(user, amount_rub, provider) → payment_url
   - process_webhook(provider, data) → bool
   - get_payment_status(payment_id) → status

6. Эндпоинты (app/api/v1/payments.py):
   POST /payments/create — создание платежа
   GET /payments/methods — доступные методы
   GET /payments/{id}/status — статус
   POST /payments/webhook/{provider} — webhook (без auth)

7. ЮKassa:
   - SDK: yookassa
   - Создание: Payment.create()
   - Webhook: notification_url

8. Robokassa:
   - Формирование URL с подписью
   - ResultURL, SuccessURL, FailURL

9. CloudPayments:
   - Widget или charge
   - Webhook: pay, fail

10. Т-Банк:
    - Init → PaymentURL
    - Webhook: Notification

11. Webhook обработка:
    a) Валидация подписи
    b) Поиск Payment по external_id
    c) Обновление статуса
    d) Если success → пополнение баланса User
    e) Создание Transaction

12. Безопасность:
    - Webhook endpoint без JWT
    - Валидация IP (опционально)
    - Валидация подписи (обязательно)
    - Логирование всех запросов

Не добавляй комментарии.
```

### 6.4 Тесты

**Тест 1 (Unit):** Создание платежа ЮKassa
```bash
docker exec easy_writer_backend python -c "
import asyncio
from app.services.payments import PaymentService
# тест с mock
"
```

**Тест 2 (Integration):** API создания платежа
```bash
curl -X POST https://api.easy-writer.ru/api/v1/payments/create \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount_rub": 100, "provider": "yookassa"}'
```

**Тест 3 (Manual):** Тестовый платёж
```
1. Создать платёж
2. Оплатить тестовой картой
3. Проверить баланс
```

### 6.5 Критерии готовности

- [ ] ЮKassa работает
- [ ] Robokassa работает
- [ ] CloudPayments работает
- [ ] Т-Банк работает
- [ ] Webhook обновляет баланс
- [ ] Транзакции записываются

---

## ЭТАП 7: БАЛАНСЫ И ТАРИФЫ

**Длительность:** 4 часа

### 7.1 Задачи

- [ ] Эндпоинты профиля
- [ ] История транзакций
- [ ] Проверка баланса при генерации

### 7.2 Промпт для Cursor AI

```
Добавь управление балансом в Easy Writer Backend.

Требования:
1. Эндпоинты (app/api/v1/user.py):
   GET /user/profile — профиль пользователя
   PUT /user/profile — обновление (name)
   GET /user/balance — текущий баланс + курс
   GET /user/transactions — история транзакций
   PUT /user/password — смена пароля

2. BalanceService (app/services/balance.py):
   - get_balance(user_id) → int
   - topup(user_id, amount, payment_id) → Transaction
   - spend(user_id, amount, description) → Transaction
   - check_balance(user_id, amount) → bool

3. Интеграция с генерацией:
   - Перед execute проверять баланс
   - После execute списывать стоимость
   - Если баланса не хватает → 402 Payment Required

4. Пагинация транзакций:
   - limit, offset
   - Сортировка по дате (DESC)

5. Ответ GET /user/balance:
   {
     "balance": 1500,
     "currency": "raits",
     "exchange_rate": 10,  # 1 RUB = 10 Raits
     "pending_payments": 0
   }

6. Ответ GET /user/transactions:
   {
     "transactions": [...],
     "pagination": {
       "total": 100,
       "limit": 20,
       "offset": 0,
       "has_more": true
     }
   }

Не добавляй комментарии.
```

### 7.3 Тесты

**Тест 1 (Unit):** Списание баланса
```bash
docker exec easy_writer_backend python -c "
import asyncio
from app.services.balance import BalanceService
# тест списания
"
```

**Тест 2 (Integration):** API баланса
```bash
curl https://api.easy-writer.ru/api/v1/user/balance \
  -H "Authorization: Bearer <token>"
```

**Тест 3 (Manual):** Генерация с недостаточным балансом
```
1. Установить баланс = 0
2. Попытаться сгенерировать
3. Проверить: ошибка 402
```

### 7.4 Критерии готовности

- [ ] Баланс отображается
- [ ] Транзакции записываются
- [ ] Пагинация работает
- [ ] 402 при недостатке баланса

---

## ЭТАП 8: WEBSOCKET

**Длительность:** 4 часа

### 8.1 Задачи

- [ ] WebSocket для прогресса генерации
- [ ] WebSocket для изображений
- [ ] Аутентификация WS

### 8.2 Промпт для Cursor AI

```
Добавь WebSocket в Easy Writer Backend.

Требования:
1. WebSocket эндпоинты:
   /ws/generation/{session_id} — прогресс генерации
   /ws/image/{image_id} — прогресс изображения

2. Аутентификация:
   - Token в query: ?token=...
   - Валидировать JWT
   - Проверять владельца сессии

3. События генерации:
   {"event": "connected", "session_id": "..."}
   {"event": "step_started", "step": 1, "step_name": "Анализ"}
   {"event": "step_progress", "step": 1, "progress": 50}
   {"event": "step_completed", "step": 1}
   {"event": "completed", "result": "..."}
   {"event": "error", "code": "...", "message": "..."}

4. События изображения:
   {"event": "connected", "image_id": "..."}
   {"event": "processing", "progress": 30}
   {"event": "completed", "url": "..."}
   {"event": "error", "code": "...", "message": "..."}

5. WebSocket Manager (app/core/websocket.py):
   - connect(websocket, session_id)
   - disconnect(session_id)
   - send_event(session_id, event)

6. Интеграция с Celery:
   - Таск отправляет события через Redis pub/sub
   - WebSocket слушает и пересылает клиенту

7. Таймаут соединения: 5 минут без активности

8. Heartbeat: ping каждые 30 сек

Не добавляй комментарии.
```

### 8.3 Тесты

**Тест 1 (Unit):** WebSocket Manager
```bash
docker exec easy_writer_backend python -c "
from app.core.websocket import WebSocketManager
manager = WebSocketManager()
print('Manager ready')
"
```

**Тест 2 (Integration):** Подключение
```javascript
// В браузере
const ws = new WebSocket('wss://api.easy-writer.ru/ws/generation/test?token=...');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

**Тест 3 (Manual):** Полный flow
```
1. Запустить standard генерацию
2. Подключиться к WebSocket
3. Проверить события по шагам
```

### 8.4 Критерии готовности

- [ ] WebSocket подключение работает
- [ ] Аутентификация по токену
- [ ] События генерации отправляются
- [ ] События изображений отправляются
- [ ] Heartbeat работает

---

## ЭТАП 9: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ

**Длительность:** 6 часов

### 9.1 Задачи

- [ ] Unit тесты (pytest)
- [ ] Integration тесты
- [ ] Нагрузочное тестирование (базовое)
- [ ] Обновление документации

### 9.2 Промпт для Cursor AI

```
Создай тесты для Easy Writer Backend.

Требования:
1. Структура тестов:
   tests/
   ├── unit/
   │   ├── test_auth.py
   │   ├── test_tools.py
   │   ├── test_generation.py
   │   ├── test_images.py
   │   ├── test_payments.py
   │   └── test_balance.py
   ├── integration/
   │   ├── test_api_auth.py
   │   ├── test_api_tools.py
   │   ├── test_api_generation.py
   │   └── test_api_payments.py
   └── conftest.py

2. conftest.py:
   - Фикстура: test database
   - Фикстура: test client (httpx AsyncClient)
   - Фикстура: test user с токеном
   - Фикстура: mock AI providers

3. pytest.ini:
   asyncio_mode = auto
   markers: unit, integration

4. Покрытие > 80%

5. Makefile:
   make test-unit
   make test-integration
   make test-all
   make coverage

6. GitHub Actions обновить:
   - Добавить тесты в CI
   - Запускать при PR

Не добавляй комментарии.
```

### 9.3 Тесты

**Тест 1 (Unit):** Все unit тесты
```bash
docker exec easy_writer_backend pytest tests/unit -v --cov=app
```

**Тест 2 (Integration):** API тесты
```bash
docker exec easy_writer_backend pytest tests/integration -v
```

**Тест 3 (Manual):** E2E через Postman
```
1. Импортировать коллекцию
2. Запустить все запросы
3. Проверить результаты
```

### 9.4 Критерии готовности

- [ ] Unit тесты > 80% coverage
- [ ] Integration тесты проходят
- [ ] CI обновлён
- [ ] Документация актуальна

---

## ЧЕКЛИСТ ЗАВЕРШЕНИЯ

### Новый функционал
- [ ] Регистрация пользователей (JWT)
- [ ] OAuth (Google, Yandex)
- [ ] 5 табов, ~35 инструментов
- [ ] GigaChat интеграция
- [ ] YandexGPT интеграция
- [ ] Kandinsky (изображения)
- [ ] 4 платёжные системы
- [ ] Балансы и транзакции
- [ ] WebSocket

### Совместимость
- [ ] WordPress API работает (не сломано)
- [ ] SQLAdmin обновлён
- [ ] Документация API актуальна

### Качество
- [ ] Тесты > 80% coverage
- [ ] Логирование через loguru
- [ ] Обработка ошибок

---

**Конец документа**

**Версия:** 2.0  
**Дата:** Декабрь 2024
