# Docker Setup для Easy Writer Web Component

## Обзор

Easy Writer Web Component работает в той же Docker сети, что и основной бекенд (`ai-article-backend`), используя общие сервисы PostgreSQL и Redis.

## Архитектура

```
┌─────────────────────────────────────────────────────────┐
│              easy-writer-network (bridge)                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ai-article-backend:                                     │
│  ├── easy_writer_backend (port 8000)                    │
│  ├── easy_writer_celery_worker                          │
│  ├── easy_writer_postgres (port 5433) ← ОБЩИЙ           │
│  └── easy_writer_redis (port 6380) ← ОБЩИЙ              │
│                                                          │
│  easy-wryter (web component):                           │
│  ├── easy_wryter_backend (port 8001)                    │
│  └── easy_wryter_celery_worker                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Требования

1. Основной бекенд `ai-article-backend` должен быть запущен и создал сеть `easy-writer-network`
2. PostgreSQL и Redis должны быть доступны в сети

## Быстрый старт

### 1. Настройка переменных окружения

```bash
cp .env.example .env
# Отредактируйте .env и укажите:
# - POSTGRES_PASSWORD (должен совпадать с основным бекендом)
# - SECRET_KEY
# - API ключи для AI провайдеров
```

### 2. Создание базы данных

Подключитесь к PostgreSQL и создайте отдельную БД для компонента:

```bash
docker exec -it easy_writer_postgres psql -U easy_writer -d postgres

CREATE DATABASE easy_wryter_db;
\q
```

### 3. Запуск контейнеров

```bash
docker-compose up -d
```

### 4. Проверка статуса

```bash
docker-compose ps
curl http://localhost:8001/health
```

## Использование общих сервисов

### PostgreSQL

- **Контейнер:** `easy_writer_postgres`
- **Порт хоста:** 5433
- **Порт контейнера:** 5432
- **База данных:** `easy_wryter_db` (отдельная БД)
- **Пользователь:** `easy_writer` (общий)

### Redis

- **Контейнер:** `easy_writer_redis`
- **Порт хоста:** 6380
- **Порт контейнера:** 6379
- **Базы данных:**
  - `0` - общий кэш (REDIS_URL)
  - `4` - Celery broker (CELERY_BROKER_URL)
  - `5` - Celery results (CELERY_RESULT_BACKEND)

**Примечание:** Основной бекенд использует базы 0, 2, 3, поэтому easy-wryter использует 4, 5 для избежания конфликтов.

## Полезные команды

### Просмотр логов

```bash
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

### Остановка

```bash
docker-compose down
```

### Перезапуск

```bash
docker-compose restart backend celery-worker
```

### Выполнение миграций

```bash
docker-compose exec backend alembic upgrade head
```

## Troubleshooting

### Ошибка: network easy-writer-network not found

Убедитесь, что основной бекенд запущен:

```bash
cd /Users/aleksey/git_projects/ai-article-backend
docker-compose up -d
```

### Ошибка подключения к PostgreSQL

Проверьте, что:
1. Контейнер `easy_writer_postgres` запущен
2. Пароль в `.env` совпадает с основным бекендом
3. База данных `easy_wryter_db` создана

### Ошибка подключения к Redis

Проверьте, что контейнер `easy_writer_redis` запущен:

```bash
docker ps | grep redis
```

