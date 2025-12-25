# API INTEGRATION SPECIFICATION v2

## Easy Writer — Спецификация API

**Версия:** 2.0  
**Дата:** Декабрь 2024  
**Статус:** MVP

---

## СОДЕРЖАНИЕ

1. [Общие принципы](#1-общие-принципы)
2. [Аутентификация](#2-аутентификация)
3. [Табы и инструменты](#3-табы-и-инструменты)
4. [Генерация контента](#4-генерация-контента)
5. [Генерация изображений](#5-генерация-изображений)
6. [WebSocket](#6-websocket)
7. [Модели данных](#7-модели-данных)
8. [Коды ошибок](#8-коды-ошибок)

---

## 1. ОБЩИЕ ПРИНЦИПЫ

### 1.1 Базовый URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.easy-writer.ru/api/v1
```

### 1.2 Формат данных

- Content-Type: `application/json`
- Кодировка: UTF-8
- Даты: ISO 8601 (`2024-12-18T10:30:00Z`)

### 1.3 Структура ответов

**Успешный ответ:**
```json
{
  "success": true,
  "data": { },
  "meta": {
    "timestamp": "2024-12-18T10:30:00Z",
    "request_id": "uuid"
  }
}
```

**Ответ с ошибкой:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Описание ошибки",
    "details": { }
  },
  "meta": {
    "timestamp": "2024-12-18T10:30:00Z",
    "request_id": "uuid"
  }
}
```

### 1.4 HTTP коды

| Код | Значение |
|-----|----------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## 2. АУТЕНТИФИКАЦИЯ

### 2.1 Регистрация

```
POST /auth/register
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "provider": "local",
      "is_verified": false,
      "created_at": "2024-12-18T10:30:00Z"
    },
    "access_token": "eyJhbG...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

**Cookies:**
- `refresh_token` (httpOnly, secure, SameSite=Lax, 7 days)

---

### 2.2 Вход

```
POST /auth/login
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "provider": "local"
    },
    "access_token": "eyJhbG...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

---

### 2.3 Обновление токена

```
POST /auth/refresh
```

**Request:** (без body, refresh_token из cookie)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbG...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

---

### 2.4 Выход

```
POST /auth/logout
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Logged out successfully"
  }
}
```

---

### 2.5 Текущий пользователь

```
GET /auth/me
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "provider": "local",
    "is_verified": true,
    "created_at": "2024-12-18T10:30:00Z"
  }
}
```

---

### 2.6 OAuth Google

```
GET /auth/google
```
Редирект на Google OAuth.

```
GET /auth/google/callback?code=...&state=...
```
Callback. Устанавливает токены и редиректит на frontend.

---

### 2.7 OAuth Yandex

```
GET /auth/yandex
```
Редирект на Yandex OAuth.

```
GET /auth/yandex/callback?code=...
```
Callback. Устанавливает токены и редиректит на frontend.

---

## 3. ТАБЫ И ИНСТРУМЕНТЫ

### 3.1 Получение списка табов

```
GET /tools/tabs
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "tabs": [
      {
        "id": "everyday",
        "name": "На каждый день",
        "description": "Инструменты для повседневных задач",
        "icon": "sun",
        "tools_count": 8
      },
      {
        "id": "education",
        "name": "Обучение",
        "description": "Инструменты для учёбы",
        "icon": "graduation-cap",
        "tools_count": 8
      },
      {
        "id": "business",
        "name": "Бизнес",
        "description": "Инструменты для бизнеса",
        "icon": "briefcase",
        "tools_count": 6
      },
      {
        "id": "marketing",
        "name": "Маркетинг",
        "description": "Инструменты для маркетинга",
        "icon": "megaphone",
        "tools_count": 7
      },
      {
        "id": "special",
        "name": "Особый случай",
        "description": "Специальные инструменты",
        "icon": "sparkles",
        "tools_count": 6
      }
    ]
  }
}
```

---

### 3.2 Получение инструментов таба

```
GET /tools/tabs/{tab_id}
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "tab": {
      "id": "everyday",
      "name": "На каждый день"
    },
    "tools": [
      {
        "id": "spell_check",
        "name": "Проверка орфографии",
        "description": "Проверка и исправление ошибок в тексте",
        "icon": "check-circle",
        "supports_modes": ["quick"],
        "recommended_provider": "gigachat"
      },
      {
        "id": "paraphrase",
        "name": "Пересказ",
        "description": "Пересказ текста своими словами",
        "icon": "refresh",
        "supports_modes": ["quick", "standard"],
        "recommended_provider": "gigachat"
      }
    ]
  }
}
```

---

### 3.3 Схема инструмента

```
GET /tools/{tool_id}/schema
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "tool_id": "spell_check",
    "name": "Проверка орфографии",
    "input_schema": {
      "type": "object",
      "required": ["text"],
      "properties": {
        "text": {
          "type": "string",
          "minLength": 1,
          "maxLength": 10000,
          "title": "Текст",
          "description": "Текст для проверки"
        }
      }
    },
    "supports_modes": ["quick"],
    "output_format": "markdown"
  }
}
```

---

### 3.4 Выполнение инструмента

```
POST /tools/{tool_id}/execute
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "input": {
    "text": "Превет мир, как дила?"
  },
  "mode": "quick",
  "provider": "auto"
}
```

**Response (200) — Quick mode:**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "status": "completed",
    "result": "Привет мир, как дела?",
    "output_format": "text",
    "provider_used": "gigachat",
    "tokens_used": 45,
    "execution_time_ms": 1230
  }
}
```

**Response (202) — Standard mode:**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "status": "in_progress",
    "websocket_url": "/ws/generation/uuid",
    "estimated_time_seconds": 30
  }
}
```

---

## 4. ГЕНЕРАЦИЯ КОНТЕНТА

### 4.1 Получение сессии

```
GET /generation/sessions/{session_id}
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "tool_id": "essay",
    "mode": "standard",
    "status": "completed",
    "input_data": {
      "topic": "Влияние технологий на образование"
    },
    "result": "# Влияние технологий на образование\n\n...",
    "output_format": "markdown",
    "provider_used": "openai",
    "tokens_used": 1250,
    "steps_completed": 4,
    "steps_total": 4,
    "created_at": "2024-12-18T10:30:00Z",
    "completed_at": "2024-12-18T10:31:15Z"
  }
}
```

---

### 4.2 Список сессий пользователя

```
GET /generation/sessions?limit=10&offset=0&status=completed
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "session_id": "uuid",
        "tool_id": "essay",
        "tool_name": "Эссе",
        "status": "completed",
        "preview": "Влияние технологий на образование...",
        "tokens_used": 1250,
        "created_at": "2024-12-18T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 10,
      "offset": 0,
      "has_more": true
    }
  }
}
```

---

### 4.3 Удаление сессии

```
DELETE /generation/sessions/{session_id}
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Session deleted"
  }
}
```

---

## 5. ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЙ

### 5.1 Генерация изображения

```
POST /images/generate
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "prompt": "Красивый закат над морем в стиле импрессионизма",
  "format": "web",
  "style": "DEFAULT"
}
```

**Форматы:**
| format | Размер | Описание |
|--------|--------|----------|
| web | 1024x1024 | Для веб |
| banner | 2048x1024 | Баннер 2:1 |
| print | 2048x2048 | Для печати |
| messenger | 512x512 | Для мессенджеров |

**Response (202):**
```json
{
  "success": true,
  "data": {
    "image_id": "uuid",
    "status": "processing",
    "websocket_url": "/ws/image/uuid",
    "estimated_time_seconds": 30
  }
}
```

---

### 5.2 Получение изображения

```
GET /images/{image_id}
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "image_id": "uuid",
    "status": "completed",
    "prompt": "Красивый закат над морем",
    "format": "web",
    "width": 1024,
    "height": 1024,
    "original_url": "/uploads/images/uuid_original.png",
    "upscaled_url": null,
    "provider": "kandinsky",
    "created_at": "2024-12-18T10:30:00Z"
  }
}
```

---

### 5.3 Апскейл изображения

```
POST /images/{image_id}/upscale
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "scale": 4,
  "target_format": "print"
}
```

**Response (202):**
```json
{
  "success": true,
  "data": {
    "image_id": "uuid",
    "status": "processing",
    "target_width": 4096,
    "target_height": 4096
  }
}
```

---

### 5.4 Поздравительная открытка

```
POST /tools/greeting_card/execute
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "input": {
    "occasion": "birthday",
    "recipient_name": "Даниил",
    "style": "веселый",
    "include_image": true,
    "image_format": "messenger"
  },
  "mode": "quick"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "status": "completed",
    "result": {
      "greeting_text": "Дорогой Даниил!\n\nС Днём рождения! Пусть этот день...",
      "image": {
        "image_id": "uuid",
        "url": "/uploads/images/uuid.png",
        "width": 512,
        "height": 512
      }
    }
  }
}
```

---

### 5.5 Список изображений

```
GET /images?limit=10&offset=0
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "images": [
      {
        "image_id": "uuid",
        "prompt": "Красивый закат...",
        "thumbnail_url": "/uploads/images/uuid_thumb.png",
        "format": "web",
        "created_at": "2024-12-18T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 15,
      "limit": 10,
      "offset": 0,
      "has_more": true
    }
  }
}
```

---

## 6. WEBSOCKET

### 6.1 Подключение к генерации

```
WS /ws/generation/{session_id}
```

**События от сервера:**

```json
{"event": "connected", "session_id": "uuid"}
```

```json
{"event": "step_started", "step": 1, "step_name": "Анализ задачи", "total_steps": 4}
```

```json
{"event": "step_progress", "step": 1, "progress": 50}
```

```json
{"event": "step_completed", "step": 1, "step_name": "Анализ задачи", "data": {"plan": "..."}}
```

```json
{"event": "completed", "result": "...", "tokens_used": 1250}
```

```json
{"event": "error", "code": "GENERATION_FAILED", "message": "..."}
```

---

### 6.2 Подключение к генерации изображения

```
WS /ws/image/{image_id}
```

**События от сервера:**

```json
{"event": "connected", "image_id": "uuid"}
```

```json
{"event": "processing", "progress": 30, "message": "Генерация..."}
```

```json
{"event": "completed", "url": "/uploads/images/uuid.png"}
```

```json
{"event": "error", "code": "IMAGE_GENERATION_FAILED", "message": "..."}
```

---

## 7. МОДЕЛИ ДАННЫХ

### 7.1 User

```typescript
interface User {
  id: string;           // UUID
  email: string;
  provider: "local" | "google" | "yandex";
  is_verified: boolean;
  created_at: string;   // ISO 8601
}
```

### 7.2 Tab

```typescript
interface Tab {
  id: string;
  name: string;
  description: string;
  icon: string;
  tools_count: number;
}
```

### 7.3 Tool

```typescript
interface Tool {
  id: string;
  name: string;
  description: string;
  icon: string;
  supports_modes: ("quick" | "standard")[];
  recommended_provider: "gigachat" | "yandexgpt" | "openai" | "auto";
}
```

### 7.4 GenerationSession

```typescript
interface GenerationSession {
  session_id: string;
  tool_id: string;
  mode: "quick" | "standard";
  status: "draft" | "in_progress" | "completed" | "failed";
  input_data: Record<string, any>;
  result: string | null;
  output_format: "text" | "markdown" | "json";
  provider_used: string;
  tokens_used: number;
  steps_completed: number;
  steps_total: number;
  created_at: string;
  completed_at: string | null;
}
```

### 7.5 GeneratedImage

```typescript
interface GeneratedImage {
  image_id: string;
  status: "processing" | "completed" | "failed";
  prompt: string;
  format: "web" | "banner" | "print" | "messenger";
  width: number;
  height: number;
  original_url: string;
  upscaled_url: string | null;
  provider: "kandinsky";
  created_at: string;
}
```

---

## 8. КОДЫ ОШИБОК

### 8.1 Аутентификация

| Код | HTTP | Описание |
|-----|------|----------|
| INVALID_CREDENTIALS | 401 | Неверный email или пароль |
| TOKEN_EXPIRED | 401 | Токен истёк |
| TOKEN_INVALID | 401 | Невалидный токен |
| USER_NOT_FOUND | 404 | Пользователь не найден |
| EMAIL_ALREADY_EXISTS | 400 | Email уже зарегистрирован |
| OAUTH_FAILED | 400 | Ошибка OAuth |

### 8.2 Инструменты

| Код | HTTP | Описание |
|-----|------|----------|
| TAB_NOT_FOUND | 404 | Таб не найден |
| TOOL_NOT_FOUND | 404 | Инструмент не найден |
| VALIDATION_ERROR | 400 | Ошибка валидации входных данных |
| INVALID_MODE | 400 | Неподдерживаемый режим |

### 8.3 Генерация

| Код | HTTP | Описание |
|-----|------|----------|
| SESSION_NOT_FOUND | 404 | Сессия не найдена |
| GENERATION_FAILED | 500 | Ошибка генерации |
| PROVIDER_UNAVAILABLE | 503 | Провайдер недоступен |
| CONTENT_BLOCKED | 400 | Контент заблокирован модерацией |
| RATE_LIMIT_EXCEEDED | 429 | Превышен лимит запросов |

### 8.4 Изображения

| Код | HTTP | Описание |
|-----|------|----------|
| IMAGE_NOT_FOUND | 404 | Изображение не найдено |
| IMAGE_GENERATION_FAILED | 500 | Ошибка генерации изображения |
| UPSCALE_FAILED | 500 | Ошибка апскейла |
| INVALID_FORMAT | 400 | Неподдерживаемый формат |

---

## ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ

### Полный flow генерации статьи (Standard mode)

```javascript
// 1. Запуск генерации
const response = await fetch('/api/v1/tools/essay/execute', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    input: { topic: 'Влияние ИИ на образование', length: 'medium' },
    mode: 'standard',
    provider: 'auto'
  })
});

const { data } = await response.json();
const sessionId = data.session_id;

// 2. Подключение к WebSocket
const ws = new WebSocket(`wss://api.easy-writer.ru/ws/generation/${sessionId}`);

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  
  switch (msg.event) {
    case 'step_started':
      console.log(`Шаг ${msg.step}/${msg.total_steps}: ${msg.step_name}`);
      break;
    case 'step_completed':
      console.log(`Шаг ${msg.step} завершён`);
      break;
    case 'completed':
      console.log('Результат:', msg.result);
      ws.close();
      break;
    case 'error':
      console.error('Ошибка:', msg.message);
      ws.close();
      break;
  }
};

// 3. Получение результата (альтернатива WebSocket)
const result = await fetch(`/api/v1/generation/sessions/${sessionId}`, {
  headers: { 'Authorization': `Bearer ${accessToken}` }
});
```

### Генерация поздравительной открытки

```javascript
const response = await fetch('/api/v1/tools/greeting_card/execute', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    input: {
      occasion: 'birthday',
      recipient_name: 'Даниил',
      style: 'веселый',
      include_image: true,
      image_format: 'messenger'
    },
    mode: 'quick'
  })
});

const { data } = await response.json();
console.log('Текст:', data.result.greeting_text);
console.log('Картинка:', data.result.image.url);
```

---

**Конец документа**

**Версия:** 2.0  
**Дата:** Декабрь 2024
