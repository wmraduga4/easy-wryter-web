# ТЕХНИЧЕСКОЕ ЗАДАНИЕ: Easy Writer MVP

**Версия:** 1.0  
**Дата:** Декабрь 2024  
**Стек:** FastAPI + React + PostgreSQL + Redis + Docker  
**Уровень разработчика:** Middle+ / Senior-

---

## СОДЕРЖАНИЕ

1. [Общие требования](#1-общие-требования)
2. [Этап 1: Инфраструктура](#этап-1-инфраструктура)
3. [Этап 2: База данных](#этап-2-база-данных)
4. [Этап 3: Аутентификация](#этап-3-аутентификация)
5. [Этап 4: Интеграция нейросетей](#этап-4-интеграция-нейросетей)
6. [Этап 5: API табов и инструментов](#этап-5-api-табов-и-инструментов)
7. [Этап 6: Режимы генерации](#этап-6-режимы-генерации)
8. [Этап 7: Генерация изображений](#этап-7-генерация-изображений)
9. [Этап 8: Модерация контента](#этап-8-модерация-контента)
10. [Этап 9: Frontend](#этап-9-frontend)
11. [Этап 10: Финальное тестирование и деплой](#этап-10-финальное-тестирование-и-деплой)

---

## 1. ОБЩИЕ ТРЕБОВАНИЯ

### 1.1 Архитектура

```
┌─────────────────────────────────────────────────────────────────┐
│                    easy-writer-network                          │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React)     Backend (FastAPI)     Celery Worker       │
│  nginx:alpine         python:3.12           python:3.12         │
│  port: 3000           port: 8000            concurrency: 8      │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL 16        Redis 7                                   │
│  port: 5433           port: 6380                                │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 MVP Scope

**Табы (5):**
- На каждый день
- Обучение
- Бизнес
- Маркетинг
- Особый случай

**Нейросети (4):**
- GigaChat (Сбер)
- YandexGPT
- GPT-4o (OpenAI)
- Kandinsky (FusionBrain) — изображения

**Режимы генерации (2):**
- Быстрый
- Стандартный

### 1.3 Переменные окружения

```env
# Database
DATABASE_URL=postgresql+asyncpg://easy_writer:password@easy_writer_postgres:5432/easy_writer_db
POSTGRES_PASSWORD=secure_password

# Redis
REDIS_URL=redis://easy_writer_redis:6379/0
CELERY_BROKER_URL=redis://easy_writer_redis:6379/2
CELERY_RESULT_BACKEND=redis://easy_writer_redis:6379/3

# Auth
SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
YANDEX_CLIENT_ID=
YANDEX_CLIENT_SECRET=

# AI Providers
GIGACHAT_API_KEY=
GIGACHAT_SCOPE=GIGACHAT_API_PERS
YANDEXGPT_API_KEY=
YANDEXGPT_FOLDER_ID=
OPENAI_API_KEY=
OPENAI_PROXY_URL=
FUSIONBRAIN_API_KEY=
FUSIONBRAIN_SECRET_KEY=

# Upscale
UPSCALE_API_KEY=
UPSCALE_API_URL=

# App
DEBUG=false
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

### 1.4 Логирование

**Библиотека:** `loguru`

```python
from loguru import logger

logger.add(
    "logs/app_{time}.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
)
```

### 1.5 Структура проекта

```
easy-writer/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── tools.py
│   │   │   │   ├── generation.py
│   │   │   │   ├── images.py
│   │   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── dependencies.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── models/
│   │   ├── services/
│   │   │   ├── ai/
│   │   │   │   ├── base.py
│   │   │   │   ├── gigachat.py
│   │   │   │   ├── yandexgpt.py
│   │   │   │   ├── openai.py
│   │   │   │   ├── kandinsky.py
│   │   │   │   └── router.py
│   │   │   ├── generation.py
│   │   │   ├── moderation.py
│   │   │   └── upscale.py
│   │   ├── schemas/
│   │   ├── tasks/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── store/
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── .env
```

---

## ЭТАП 1: ИНФРАСТРУКТУРА

**Длительность:** 4 часа

### 1.1 Задачи

- [ ] Создать структуру проекта
- [ ] Настроить docker-compose.yml
- [ ] Настроить Dockerfile для backend
- [ ] Настроить Dockerfile для frontend
- [ ] Создать .env.example
- [ ] Настроить loguru
- [ ] Проверить healthchecks

### 1.2 Промпт для Cursor AI

```
Создай инфраструктуру для проекта Easy Writer.

Требования:
1. Docker Compose с сервисами:
   - easy_writer_frontend (nginx:alpine, port 3000)
   - easy_writer_backend (python:3.12-slim, port 8000)
   - easy_writer_postgres (postgres:16-alpine, port 5433)
   - easy_writer_redis (redis:7-alpine, port 6380)
   - easy_writer_celery_worker (python:3.12-slim)

2. Сеть: easy-writer-network (bridge)

3. Volumes:
   - easy_writer_postgres_data
   - easy_writer_redis_data

4. Backend Dockerfile (multi-stage build):
   - Base image: python:3.12-slim
   - User: appuser (UID 1000)
   - Healthcheck: curl -f http://localhost:8000/health

5. Логирование через loguru:
   - Файл: logs/app_{time}.log
   - Rotation: 500 MB
   - Retention: 10 days

6. Создай .env.example со всеми переменными из спецификации.

7. Healthchecks:
   - Backend: 30s interval, 10s timeout, 3 retries
   - Postgres: 10s interval, 5s timeout, 5 retries
   - Redis: 10s interval, 5s timeout, 5 retries

Не добавляй комментарии и пояснения в код.
```

### 1.3 Тесты

**Тест 1 (Unit):** Проверка загрузки конфигурации
```bash
docker exec easy_writer_backend python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```
Ожидаемый результат: вывод DATABASE_URL без ошибок

**Тест 2 (Integration):** Проверка связности сервисов
```bash
docker compose ps
```
Ожидаемый результат: все сервисы в статусе "healthy"

**Тест 3 (Manual):** Проверка healthcheck endpoint
```bash
curl http://localhost:8000/health
```
Ожидаемый результат: `{"status": "ok"}`

### 1.4 Критерии готовности

- [ ] `docker compose up -d` запускает все сервисы
- [ ] Все healthchecks проходят
- [ ] Логи пишутся в файл
- [ ] Backend отвечает на /health

---

## ЭТАП 2: БАЗА ДАННЫХ

**Длительность:** 6 часов

### 2.1 Задачи

- [ ] Создать модели SQLAlchemy
- [ ] Настроить Alembic
- [ ] Создать начальные миграции
- [ ] Настроить async сессии

### 2.2 Модели данных

```
User
├── id: UUID (PK)
├── email: String (unique)
├── hashed_password: String (nullable)
├── provider: Enum (local, google, yandex)
├── provider_id: String (nullable)
├── is_active: Boolean
├── is_verified: Boolean
├── created_at: DateTime
└── updated_at: DateTime

GenerationSession
├── id: UUID (PK)
├── user_id: UUID (FK → User)
├── tab: Enum (everyday, education, business, marketing, special)
├── tool: String
├── mode: Enum (quick, standard)
├── status: Enum (draft, in_progress, completed, failed)
├── input_data: JSONB
├── result: Text (nullable)
├── ai_provider: Enum (gigachat, yandexgpt, openai)
├── tokens_used: Integer
├── created_at: DateTime
└── updated_at: DateTime

GeneratedImage
├── id: UUID (PK)
├── user_id: UUID (FK → User)
├── session_id: UUID (FK → GenerationSession, nullable)
├── prompt: Text
├── provider: Enum (kandinsky)
├── original_url: String
├── upscaled_url: String (nullable)
├── format: Enum (web, banner, print, messenger)
├── width: Integer
├── height: Integer
├── created_at: DateTime
└── updated_at: DateTime

ModerationLog
├── id: UUID (PK)
├── session_id: UUID (FK → GenerationSession)
├── input_text: Text
├── is_blocked: Boolean
├── reason: String (nullable)
├── created_at: DateTime
└── updated_at: DateTime
```

### 2.3 Промпт для Cursor AI

```
Создай модели SQLAlchemy и настрой Alembic для Easy Writer.

Требования:
1. Async SQLAlchemy 2.0 с asyncpg
2. Модели: User, GenerationSession, GeneratedImage, ModerationLog (схема выше)
3. UUID как первичные ключи (uuid7)
4. Enum через sqlalchemy.Enum с native_enum=False
5. JSONB для input_data
6. Индексы: user_id, created_at, status
7. Alembic с async поддержкой
8. Формат имени миграций: YYYY-MM-DD_slug.py
9. Base класс с created_at, updated_at (auto)

Файлы:
- app/db/base.py — Base класс
- app/db/session.py — async session factory
- app/db/models/user.py
- app/db/models/generation.py
- app/db/models/image.py
- app/db/models/moderation.py
- alembic/env.py — async config

Не добавляй комментарии.
```

### 2.4 Тесты

**Тест 1 (Unit):** Валидация моделей
```bash
docker exec easy_writer_backend python -c "
from app.db.models.user import User
from app.db.models.generation import GenerationSession
print('Models OK')
"
```

**Тест 2 (Integration):** Применение миграций
```bash
docker exec easy_writer_backend alembic upgrade head
docker exec easy_writer_backend alembic current
```
Ожидаемый результат: миграция применена, текущая версия отображается

**Тест 3 (Manual):** Проверка таблиц в БД
```bash
docker exec easy_writer_postgres psql -U easy_writer -d easy_writer_db -c "\dt"
```
Ожидаемый результат: таблицы users, generation_sessions, generated_images, moderation_logs

### 2.5 Критерии готовности

- [ ] Все модели созданы
- [ ] Миграции применяются без ошибок
- [ ] Таблицы существуют в БД
- [ ] Индексы созданы

---

## ЭТАП 3: АУТЕНТИФИКАЦИЯ

**Длительность:** 8 часов

### 3.1 Задачи

- [ ] JWT аутентификация (access + refresh tokens)
- [ ] Регистрация по email + пароль
- [ ] OAuth Google
- [ ] OAuth Yandex
- [ ] Эндпоинты: register, login, refresh, logout, me

### 3.2 Промпт для Cursor AI

```
Создай систему аутентификации для Easy Writer.

Требования:
1. JWT токены:
   - Access token: 15 минут, в response body
   - Refresh token: 7 дней, httpOnly cookie
   - Алгоритм: HS256

2. Эндпоинты:
   POST /api/v1/auth/register — регистрация (email, password)
   POST /api/v1/auth/login — вход (email, password) → tokens
   POST /api/v1/auth/refresh — обновление access token
   POST /api/v1/auth/logout — выход (удаление refresh cookie)
   GET /api/v1/auth/me — текущий пользователь

3. OAuth:
   GET /api/v1/auth/google — редирект на Google
   GET /api/v1/auth/google/callback — callback
   GET /api/v1/auth/yandex — редирект на Yandex
   GET /api/v1/auth/yandex/callback — callback

4. Библиотеки:
   - python-jose[cryptography] для JWT
   - passlib[bcrypt] для паролей
   - httpx для OAuth

5. Dependency: get_current_user для защищённых эндпоинтов

6. Валидация email через pydantic EmailStr

7. Пароль: минимум 8 символов

Файлы:
- app/core/security.py — JWT, password hashing
- app/api/v1/auth.py — эндпоинты
- app/schemas/auth.py — Pydantic схемы
- app/services/auth.py — бизнес-логика

Не добавляй комментарии.
```

### 3.3 Тесты

**Тест 1 (Unit):** Хеширование пароля
```bash
docker exec easy_writer_backend python -c "
from app.core.security import hash_password, verify_password
h = hash_password('test123456')
assert verify_password('test123456', h)
print('Password hashing OK')
"
```

**Тест 2 (Integration):** Регистрация и логин
```bash
# Регистрация
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123456"}'

# Логин
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123456"}'
```
Ожидаемый результат: access_token в ответе

**Тест 3 (Manual):** OAuth flow
```
1. Открыть http://localhost:8000/api/v1/auth/google
2. Авторизоваться в Google
3. Проверить редирект и получение токенов
```

### 3.4 Критерии готовности

- [ ] Регистрация работает
- [ ] Логин возвращает токены
- [ ] Refresh token обновляет access token
- [ ] OAuth Google работает
- [ ] OAuth Yandex работает
- [ ] Защищённые эндпоинты требуют токен

---

## ЭТАП 4: ИНТЕГРАЦИЯ НЕЙРОСЕТЕЙ

**Длительность:** 12 часов

### 4.1 Задачи

- [ ] Базовый класс AIProvider
- [ ] Интеграция GigaChat
- [ ] Интеграция YandexGPT
- [ ] Интеграция OpenAI (GPT-4o)
- [ ] Роутер выбора провайдера
- [ ] Кэширование токенов GigaChat в Redis

### 4.2 Промпт для Cursor AI

```
Создай систему интеграции с нейросетями для Easy Writer.

Требования:
1. Базовый класс AIProvider (abc):
   - async generate(prompt: str, system: str, **kwargs) → str
   - async count_tokens(text: str) → int
   - name: str
   - max_tokens: int

2. GigaChat (app/services/ai/gigachat.py):
   - OAuth токен кэшировать в Redis (TTL 25 минут)
   - Endpoint: https://gigachat.devices.sberbank.ru/api/v1
   - Scope из env: GIGACHAT_SCOPE
   - SSL verify: certificates/russian_trusted_root_ca.cer

3. YandexGPT (app/services/ai/yandexgpt.py):
   - Endpoint: https://llm.api.cloud.yandex.net/foundationModels/v1/completion
   - Model: yandexgpt-lite или yandexgpt
   - Folder ID из env

4. OpenAI (app/services/ai/openai.py):
   - Proxy URL из env (OPENAI_PROXY_URL)
   - Model: gpt-4o
   - Использовать openai SDK

5. Роутер (app/services/ai/router.py):
   - select_provider(task_type: str, language: str) → AIProvider
   - Логика:
     - Русский + простые задачи → GigaChat
     - Академические → OpenAI
     - SEO/маркетинг → OpenAI
     - fallback при ошибке → следующий провайдер

6. Retry логика: 3 попытки с exponential backoff

7. Логирование через loguru: prompt, provider, tokens, latency

Файлы:
- app/services/ai/base.py
- app/services/ai/gigachat.py
- app/services/ai/yandexgpt.py
- app/services/ai/openai.py
- app/services/ai/router.py

Не добавляй комментарии.
```

### 4.3 Тесты

**Тест 1 (Unit):** Инициализация провайдеров
```bash
docker exec easy_writer_backend python -c "
from app.services.ai.gigachat import GigaChatProvider
from app.services.ai.yandexgpt import YandexGPTProvider
from app.services.ai.openai import OpenAIProvider
print('Providers initialized')
"
```

**Тест 2 (Integration):** Генерация текста
```bash
docker exec easy_writer_backend python -c "
import asyncio
from app.services.ai.gigachat import GigaChatProvider

async def test():
    provider = GigaChatProvider()
    result = await provider.generate('Привет, как дела?', 'Ты помощник.')
    print(result[:100])

asyncio.run(test())
"
```

**Тест 3 (Manual):** Проверка роутера
```bash
docker exec easy_writer_backend python -c "
from app.services.ai.router import AIRouter

router = AIRouter()
provider = router.select_provider('essay', 'ru')
print(f'Selected: {provider.name}')
"
```

### 4.4 Критерии готовности

- [ ] GigaChat генерирует текст
- [ ] YandexGPT генерирует текст
- [ ] OpenAI генерирует текст
- [ ] Роутер выбирает провайдера
- [ ] Токен GigaChat кэшируется в Redis
- [ ] Retry работает при ошибках

---

## ЭТАП 5: API ТАБОВ И ИНСТРУМЕНТОВ

**Длительность:** 10 часов

### 5.1 Задачи

- [ ] Структура табов и инструментов
- [ ] Эндпоинты для получения списка инструментов
- [ ] Эндпоинт запуска инструмента
- [ ] Промпты для каждого инструмента

### 5.2 Структура табов

```python
TABS = {
    "everyday": {
        "name": "На каждый день",
        "tools": [
            "spell_check",      # Проверка орфографии
            "paraphrase",       # Пересказ
            "simplify",         # Упрощение
            "letter",           # Письмо
            "social_post",      # Пост для соцсетей
            "resume",           # Резюме
            "summarize",        # Краткое изложение
            "translate"         # Перевод
        ]
    },
    "education": {
        "name": "Обучение",
        "tools": [
            "essay",            # Сочинение
            "essay_academic",   # Эссе
            "report",           # Доклад
            "abstract",         # Реферат
            "notes",            # Конспект
            "retelling",        # Пересказ текста
            "qa_text",          # Ответы на вопросы
            "spell_check"       # Проверка орфографии
        ]
    },
    "business": {
        "name": "Бизнес",
        "tools": [
            "contract_generate",    # Генерация договора
            "contract_analyze",     # Анализ договора
            "commercial_offer",     # Коммерческое предложение
            "business_letter",      # Деловое письмо
            "meeting_notes",        # Протокол встречи
            "presentation_text"     # Текст презентации
        ]
    },
    "marketing": {
        "name": "Маркетинг",
        "tools": [
            "seo_article",          # SEO-статья
            "product_description",  # Описание товара
            "email_campaign",       # Email-рассылка
            "landing_text",         # Текст лендинга
            "press_release",        # Пресс-релиз
            "slogan",               # Слоган
            "naming"                # Нейминг
        ]
    },
    "special": {
        "name": "Особый случай",
        "tools": [
            "custom_prompt",        # Кастомный промпт
            "greeting_card",        # Поздравление + картинка
            "toast",                # Тост
            "speech",               # Речь
            "image_generate",       # Генерация изображения
            "image_upscale"         # Апскейл изображения
        ]
    }
}
```

### 5.3 Промпт для Cursor AI

```
Создай API табов и инструментов для Easy Writer.

Требования:
1. Эндпоинты:
   GET /api/v1/tools/tabs — список табов
   GET /api/v1/tools/tabs/{tab_id} — инструменты таба
   GET /api/v1/tools/{tool_id}/schema — схема входных данных инструмента
   POST /api/v1/tools/{tool_id}/execute — запуск инструмента

2. Структура табов из спецификации выше

3. Каждый инструмент имеет:
   - id: str
   - name: str (человекочитаемое)
   - description: str
   - input_schema: dict (JSON Schema)
   - recommended_provider: str
   - supports_modes: list[str]

4. Промпты инструментов хранить в YAML:
   prompts/
   ├── everyday/
   │   ├── spell_check.yaml
   │   └── ...
   ├── education/
   ├── business/
   ├── marketing/
   └── special/

5. Формат YAML:
   system: "Системный промпт"
   user_template: "Шаблон с {переменными}"
   output_format: "text" | "json" | "markdown"
   max_tokens: 2000

6. Execute эндпоинт:
   - Валидация input по schema
   - Выбор провайдера
   - Генерация
   - Сохранение в GenerationSession
   - Возврат результата

7. Защита: require get_current_user

Файлы:
- app/api/v1/tools.py
- app/services/tools.py
- app/schemas/tools.py
- prompts/**/*.yaml

Не добавляй комментарии.
```

### 5.4 Тесты

**Тест 1 (Unit):** Загрузка промптов
```bash
docker exec easy_writer_backend python -c "
from app.services.tools import ToolService
service = ToolService()
prompt = service.get_prompt('spell_check')
print(prompt.system[:50])
"
```

**Тест 2 (Integration):** Получение списка табов
```bash
curl http://localhost:8000/api/v1/tools/tabs \
  -H "Authorization: Bearer <token>"
```

**Тест 3 (Manual):** Выполнение инструмента
```bash
curl -X POST http://localhost:8000/api/v1/tools/spell_check/execute \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Превет мир", "mode": "quick"}'
```

### 5.5 Критерии готовности

- [ ] Все табы и инструменты доступны через API
- [ ] Промпты загружаются из YAML
- [ ] Execute работает для всех инструментов
- [ ] Результаты сохраняются в БД

---

## ЭТАП 6: РЕЖИМЫ ГЕНЕРАЦИИ

**Длительность:** 6 часов

### 6.1 Задачи

- [ ] Быстрый режим (single shot)
- [ ] Стандартный режим (multi-step)
- [ ] Celery таски для стандартного режима
- [ ] WebSocket для прогресса

### 6.2 Промпт для Cursor AI

```
Создай систему режимов генерации для Easy Writer.

Требования:
1. Быстрый режим:
   - Один запрос к AI
   - Синхронный ответ
   - Для простых задач

2. Стандартный режим (4 шага):
   - Шаг 1: Анализ задачи → план
   - Шаг 2: Генерация структуры
   - Шаг 3: Генерация контента по секциям
   - Шаг 4: Финальная редактура
   
3. Celery таски:
   - generation_standard_task(session_id, step)
   - Каждый шаг — отдельный таск
   - Цепочка: step1 → step2 → step3 → step4

4. WebSocket (app/api/v1/ws.py):
   - /ws/generation/{session_id}
   - События: step_started, step_completed, error, done
   - Формат: {"event": "step_completed", "step": 2, "data": {...}}

5. Статусы сессии:
   - draft → in_progress → completed / failed

6. При ошибке: retry 2 раза, затем failed

7. Таймаут шага: 120 секунд

Файлы:
- app/services/generation.py
- app/tasks/generation.py
- app/api/v1/ws.py

Не добавляй комментарии.
```

### 6.3 Тесты

**Тест 1 (Unit):** Быстрая генерация
```bash
docker exec easy_writer_backend python -c "
import asyncio
from app.services.generation import GenerationService

async def test():
    service = GenerationService()
    result = await service.generate_quick('spell_check', {'text': 'тест'})
    print(result[:100])

asyncio.run(test())
"
```

**Тест 2 (Integration):** Celery таск
```bash
docker exec easy_writer_backend python -c "
from app.tasks.generation import generation_standard_task
result = generation_standard_task.delay('test-session-id', 1)
print(f'Task ID: {result.id}')
"
```

**Тест 3 (Manual):** WebSocket
```javascript
// В браузере
const ws = new WebSocket('ws://localhost:8000/ws/generation/session-id');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

### 6.4 Критерии готовности

- [ ] Быстрый режим работает синхронно
- [ ] Стандартный режим выполняется через Celery
- [ ] WebSocket отправляет события
- [ ] Статусы сессии обновляются

---

## ЭТАП 7: ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЙ

**Длительность:** 8 часов

### 7.1 Задачи

- [ ] Интеграция Kandinsky (FusionBrain)
- [ ] Апскейл через внешний API
- [ ] Форматы: web, banner, print, messenger
- [ ] Инструмент "Поздравление + картинка"

### 7.2 Промпт для Cursor AI

```
Создай систему генерации изображений для Easy Writer.

Требования:
1. Kandinsky (FusionBrain API):
   - Endpoint: https://api-key.fusionbrain.ai/
   - Auth: X-Key и X-Secret headers
   - Async генерация: POST /key/api/v1/text2image/run → GET /key/api/v1/text2image/status/{uuid}
   - Polling каждые 3 секунды, таймаут 120 секунд

2. Форматы и размеры:
   - web: 1024x1024
   - banner: 2048x1024 (2:1)
   - print: 2048x2048 (для апскейла до 300dpi)
   - messenger: 512x512

3. Апскейл:
   - Внешний API (env: UPSCALE_API_URL, UPSCALE_API_KEY)
   - Увеличение 2x или 4x
   - Для print формата — обязательный апскейл 4x

4. Инструмент greeting_card:
   - Вход: occasion (день рождения, свадьба, и т.д.), recipient_name, style
   - Шаг 1: Генерация текста поздравления (AI)
   - Шаг 2: Генерация промпта для картинки (AI)
   - Шаг 3: Генерация картинки (Kandinsky)
   - Выход: {text: str, image_url: str}

5. Эндпоинты:
   POST /api/v1/images/generate — генерация
   POST /api/v1/images/upscale — апскейл
   GET /api/v1/images/{id} — получение

6. Сохранение: GeneratedImage в БД, файлы в локальную папку /uploads/images/

7. Celery таск для генерации (долгая операция)

Файлы:
- app/services/ai/kandinsky.py
- app/services/upscale.py
- app/services/images.py
- app/api/v1/images.py
- app/tasks/images.py

Не добавляй комментарии.
```

### 7.3 Тесты

**Тест 1 (Unit):** Kandinsky клиент
```bash
docker exec easy_writer_backend python -c "
from app.services.ai.kandinsky import KandinskyProvider
provider = KandinskyProvider()
print(f'Provider: {provider.name}')
"
```

**Тест 2 (Integration):** Генерация изображения
```bash
curl -X POST http://localhost:8000/api/v1/images/generate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Красивый закат над морем", "format": "web"}'
```

**Тест 3 (Manual):** Поздравительная открытка
```bash
curl -X POST http://localhost:8000/api/v1/tools/greeting_card/execute \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"occasion": "birthday", "recipient_name": "Даниил", "style": "веселый"}'
```

### 7.4 Критерии готовности

- [ ] Kandinsky генерирует изображения
- [ ] Апскейл работает
- [ ] Все форматы поддерживаются
- [ ] Поздравительная открытка создаётся

---

## ЭТАП 8: МОДЕРАЦИЯ КОНТЕНТА

**Длительность:** 4 часа

### 8.1 Задачи

- [ ] Фильтр запрещённого контента
- [ ] Предмодерация входящих запросов
- [ ] Постмодерация результатов
- [ ] Логирование инцидентов

### 8.2 Промпт для Cursor AI

```
Создай систему модерации контента для Easy Writer.

Требования:
1. Запрещённые категории:
   - porn, sexual
   - violence, gore
   - drugs
   - extremism, terrorism
   - child_abuse
   - fraud
   - personal_data
   - malware

2. Предмодерация:
   - Проверка входного текста перед отправкой в AI
   - Keyword-based фильтр (словарь в YAML)
   - Regex паттерны

3. Постмодерация:
   - Проверка результата AI
   - Тот же фильтр

4. При блокировке:
   - Сохранить в ModerationLog
   - Вернуть ошибку CONTENT_BLOCKED
   - Не показывать причину пользователю (безопасность)

5. Словарь: moderation/blocked_keywords.yaml
   categories:
     porn: [список слов]
     violence: [список слов]
     ...

6. Middleware для автоматической проверки всех /tools/*/execute

Файлы:
- app/services/moderation.py
- app/middleware/moderation.py
- moderation/blocked_keywords.yaml

Не добавляй комментарии.
```

### 8.3 Тесты

**Тест 1 (Unit):** Проверка фильтра
```bash
docker exec easy_writer_backend python -c "
from app.services.moderation import ModerationService
service = ModerationService()
result = service.check('обычный текст')
print(f'Blocked: {result.is_blocked}')
"
```

**Тест 2 (Integration):** Блокировка запроса
```bash
# Отправить запрос с запрещённым контентом
# Ожидать: 400 CONTENT_BLOCKED
```

**Тест 3 (Manual):** Проверка логов
```bash
docker exec easy_writer_postgres psql -U easy_writer -d easy_writer_db \
  -c "SELECT * FROM moderation_logs ORDER BY created_at DESC LIMIT 5;"
```

### 8.4 Критерии готовности

- [ ] Фильтр блокирует запрещённый контент
- [ ] Middleware работает
- [ ] Инциденты логируются
- [ ] Причина не раскрывается пользователю

---

## ЭТАП 9: FRONTEND

**Длительность:** 16 часов

### 9.1 Задачи

- [ ] Структура React приложения
- [ ] Авторизация (формы + OAuth)
- [ ] Навигация по табам
- [ ] Формы инструментов
- [ ] Отображение результатов
- [ ] WebSocket интеграция

### 9.2 Промпт для Cursor AI

```
Создай React frontend для Easy Writer.

Требования:
1. Stack:
   - React 18 + TypeScript
   - Vite
   - TailwindCSS
   - React Query (TanStack)
   - Zustand (state)
   - React Router 6
   - React Hook Form + Zod

2. Структура:
   src/
   ├── components/
   │   ├── ui/ (Button, Input, Card, Modal, Tabs, ...)
   │   ├── auth/ (LoginForm, RegisterForm, OAuthButtons)
   │   ├── tools/ (ToolCard, ToolForm, ResultDisplay)
   │   └── layout/ (Header, Sidebar, Footer)
   ├── pages/
   │   ├── HomePage.tsx
   │   ├── LoginPage.tsx
   │   ├── RegisterPage.tsx
   │   ├── DashboardPage.tsx
   │   ├── ToolPage.tsx
   │   └── HistoryPage.tsx
   ├── hooks/
   │   ├── useAuth.ts
   │   ├── useTools.ts
   │   └── useWebSocket.ts
   ├── services/
   │   └── api.ts (axios instance)
   ├── store/
   │   ├── authStore.ts
   │   └── toolStore.ts
   └── types/

3. Страницы:
   - / — лендинг
   - /login — вход
   - /register — регистрация
   - /dashboard — табы и инструменты
   - /tool/:toolId — форма инструмента
   - /history — история генераций

4. Компоненты табов:
   - TabsNavigation — горизонтальные табы
   - ToolGrid — сетка инструментов таба
   - ToolCard — карточка инструмента

5. Форма инструмента:
   - Динамическая генерация из input_schema
   - Выбор режима (quick/standard)
   - Кнопка генерации
   - Прогресс (WebSocket)
   - Результат (текст/markdown/изображение)

6. Адаптивность: mobile-first

7. Тёмная тема: поддержка

Не добавляй комментарии в код.
```

### 9.3 Тесты

**Тест 1 (Unit):** Сборка проекта
```bash
cd frontend && npm run build
```

**Тест 2 (Integration):** API запросы
```
1. Открыть http://localhost:3000
2. Зарегистрироваться
3. Проверить редирект на /dashboard
```

**Тест 3 (Manual):** Полный flow
```
1. Логин
2. Выбрать таб "На каждый день"
3. Выбрать инструмент "Проверка орфографии"
4. Ввести текст
5. Нажать "Сгенерировать"
6. Увидеть результат
```

### 9.4 Критерии готовности

- [ ] Авторизация работает
- [ ] Табы отображаются
- [ ] Инструменты доступны
- [ ] Генерация работает
- [ ] WebSocket показывает прогресс
- [ ] Мобильная версия работает

---

## ЭТАП 10: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ И ДЕПЛОЙ

**Длительность:** 8 часов

### 10.1 Задачи

- [ ] Покрытие unit тестами (>80%)
- [ ] Integration тесты
- [ ] E2E тесты (базовые)
- [ ] Деплой на production
- [ ] Мониторинг

### 10.2 Промпт для Cursor AI

```
Создай тесты и настрой деплой для Easy Writer.

Требования:
1. Unit тесты (pytest):
   - tests/unit/test_auth.py
   - tests/unit/test_tools.py
   - tests/unit/test_generation.py
   - tests/unit/test_moderation.py
   - tests/unit/test_images.py
   - Покрытие >80%

2. Integration тесты:
   - tests/integration/test_api_auth.py
   - tests/integration/test_api_tools.py
   - tests/integration/test_api_generation.py
   - Использовать httpx AsyncClient
   - Test database (отдельная БД)

3. E2E тесты (Playwright):
   - tests/e2e/test_auth_flow.py
   - tests/e2e/test_generation_flow.py
   - Базовые сценарии

4. pytest.ini:
   - asyncio_mode = auto
   - markers: unit, integration, e2e

5. Makefile:
   - make test-unit
   - make test-integration
   - make test-e2e
   - make test-all
   - make coverage

6. GitHub Actions (.github/workflows/ci.yml):
   - Trigger: push to main, PR
   - Jobs: lint, test-unit, test-integration
   - Deploy: только при merge в main

7. Деплой скрипт (scripts/deploy.sh):
   - Pull latest
   - Build images
   - Run migrations
   - Restart services
   - Health check

Не добавляй комментарии.
```

### 10.3 Тесты

**Тест 1 (Unit):** Запуск всех unit тестов
```bash
docker exec easy_writer_backend pytest tests/unit -v --cov=app --cov-report=term-missing
```
Ожидаемый результат: >80% coverage, 0 failed

**Тест 2 (Integration):** API тесты
```bash
docker exec easy_writer_backend pytest tests/integration -v
```
Ожидаемый результат: все тесты прошли

**Тест 3 (Manual):** Production деплой
```bash
ssh production "cd /root/easy-writer && ./scripts/deploy.sh"
curl https://api.easy-writer.ru/health
```
Ожидаемый результат: `{"status": "ok"}`

### 10.4 Критерии готовности

- [ ] Unit тесты: >80% coverage
- [ ] Integration тесты: все проходят
- [ ] E2E тесты: базовые сценарии работают
- [ ] CI/CD настроен
- [ ] Production деплой выполнен
- [ ] Health check проходит

---

## ЧЕКЛИСТ ЗАВЕРШЕНИЯ MVP

### Backend
- [ ] Все эндпоинты работают
- [ ] Аутентификация (JWT + OAuth)
- [ ] 4 AI провайдера подключены
- [ ] 5 табов, все инструменты
- [ ] 2 режима генерации
- [ ] Генерация изображений
- [ ] Модерация работает
- [ ] Логирование через loguru
- [ ] Тесты >80%

### Frontend
- [ ] Авторизация
- [ ] Навигация по табам
- [ ] Формы инструментов
- [ ] WebSocket прогресс
- [ ] Адаптивность
- [ ] Тёмная тема

### Infrastructure
- [ ] Docker Compose работает
- [ ] Healthchecks проходят
- [ ] CI/CD настроен
- [ ] Production деплой

---

**Конец документа**

**Версия:** 1.0  
**Дата:** Декабрь 2024
