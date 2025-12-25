# API INTEGRATION SPECIFICATION v2

## Easy Writer — Контракт API

**Версия:** 2.0  
**Дата:** Декабрь 2024

---

## 1. ОБЩИЕ ПРИНЦИПЫ

### Base URL
```
Production: https://api.easy-writer.ru/api/v1
Development: http://localhost:8000/api/v1
```

### Аутентификация
```
Authorization: Bearer <access_token>
```

### Формат ответа
```json
{
  "success": true,
  "data": { },
  "meta": { "timestamp": "...", "request_id": "..." }
}
```

---

## 2. АУТЕНТИФИКАЦИЯ

### POST /auth/register
```json
// Request
{ "email": "user@example.com", "password": "pass123456" }

// Response 201
{
  "user": { "id": "uuid", "email": "...", "balance": 100 },
  "access_token": "eyJ...",
  "expires_in": 900
}
```

### POST /auth/login
```json
// Request
{ "email": "user@example.com", "password": "pass123456" }

// Response 200
{ "user": {...}, "access_token": "eyJ...", "expires_in": 900 }
```

### POST /auth/refresh
```json
// Response 200 (refresh_token из cookie)
{ "access_token": "eyJ...", "expires_in": 900 }
```

### POST /auth/logout
```json
// Response 200
{ "message": "Logged out" }
```

### GET /auth/me
```json
// Response 200
{ "id": "uuid", "email": "...", "name": "...", "provider": "local", "balance": 1500 }
```

### GET /auth/google
Редирект → Google OAuth → callback → frontend с токеном

### GET /auth/yandex
Редирект → Yandex OAuth → callback → frontend с токеном

---

## 3. ПОЛЬЗОВАТЕЛЬ

### GET /user/profile
```json
// Response 200
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Иван",
  "provider": "google",
  "balance": 1500,
  "total_generations": 42,
  "created_at": "2024-12-18T10:30:00Z"
}
```

### PUT /user/profile
```json
// Request
{ "name": "Иван Петров" }
```

### GET /user/balance
```json
// Response 200
{
  "balance": 1500,
  "currency": "raits",
  "currency_symbol": "Ꝑ",
  "exchange_rate": 10
}
```

### GET /user/transactions?limit=20&offset=0
```json
// Response 200
{
  "transactions": [
    { "id": "uuid", "type": "topup", "amount": 1000, "description": "Пополнение", "created_at": "..." },
    { "id": "uuid", "type": "spend", "amount": -15, "description": "Проверка орфографии", "created_at": "..." }
  ],
  "pagination": { "total": 50, "limit": 20, "offset": 0, "has_more": true }
}
```

### PUT /user/password
```json
// Request
{ "current_password": "old123456", "new_password": "new123456" }
```

---

## 4. ТАБЫ И ИНСТРУМЕНТЫ

### GET /tools/tabs
```json
// Response 200
{
  "tabs": [
    { "id": "everyday", "name": "На каждый день", "icon": "sun", "tools_count": 8 },
    { "id": "education", "name": "Обучение", "icon": "graduation-cap", "tools_count": 8 },
    { "id": "business", "name": "Бизнес", "icon": "briefcase", "tools_count": 6 },
    { "id": "marketing", "name": "Маркетинг", "icon": "megaphone", "tools_count": 7 },
    { "id": "special", "name": "Особый случай", "icon": "sparkles", "tools_count": 6 }
  ]
}
```

### GET /tools/tabs/{tab_id}
```json
// Response 200
{
  "tab": { "id": "everyday", "name": "На каждый день" },
  "tools": [
    {
      "id": "spell_check",
      "name": "Проверка орфографии",
      "description": "Исправление ошибок в тексте",
      "icon": "check-circle",
      "supports_modes": ["quick"],
      "estimated_cost": 5
    }
  ]
}
```

### GET /tools/{tool_id}/schema
```json
// Response 200
{
  "tool_id": "spell_check",
  "name": "Проверка орфографии",
  "input_schema": {
    "type": "object",
    "required": ["text"],
    "properties": {
      "text": { "type": "string", "minLength": 1, "maxLength": 10000, "title": "Текст" }
    }
  },
  "supports_modes": ["quick"],
  "estimated_cost": 5
}
```

### POST /tools/{tool_id}/execute
```json
// Request
{
  "input": { "text": "Превет мир" },
  "mode": "quick"
}

// Response 200 (quick mode)
{
  "session_id": "uuid",
  "status": "completed",
  "result": "Привет мир",
  "provider_used": "gigachat",
  "tokens_used": 45,
  "cost_raits": 5
}

// Response 202 (standard mode)
{
  "session_id": "uuid",
  "status": "in_progress",
  "websocket_url": "/ws/generation/uuid"
}
```

---

## 5. ГЕНЕРАЦИЯ

### GET /generation/sessions/{session_id}
```json
// Response 200
{
  "session_id": "uuid",
  "tool_id": "essay",
  "mode": "standard",
  "status": "completed",
  "input_data": { "topic": "..." },
  "result": "...",
  "provider_used": "openai",
  "tokens_used": 1250,
  "cost_raits": 50,
  "created_at": "...",
  "completed_at": "..."
}
```

### GET /generation/sessions?limit=10&offset=0
```json
// Response 200
{
  "sessions": [
    {
      "session_id": "uuid",
      "tool_id": "essay",
      "tool_name": "Эссе",
      "status": "completed",
      "preview": "Текст начинается...",
      "cost_raits": 50,
      "created_at": "..."
    }
  ],
  "pagination": { "total": 25, "limit": 10, "offset": 0, "has_more": true }
}
```

### DELETE /generation/sessions/{session_id}
```json
// Response 200
{ "message": "Deleted" }
```

---

## 6. ИЗОБРАЖЕНИЯ

### POST /images/generate
```json
// Request
{
  "prompt": "Красивый закат над морем",
  "format": "web",
  "style": "DEFAULT"
}

// Response 202
{
  "image_id": "uuid",
  "status": "processing",
  "websocket_url": "/ws/image/uuid"
}
```

**Форматы:**
| format | Размер |
|--------|--------|
| web | 1024x1024 |
| banner | 2048x1024 |
| print | 2048x2048 |
| messenger | 512x512 |

### GET /images/{image_id}
```json
// Response 200
{
  "image_id": "uuid",
  "status": "completed",
  "prompt": "...",
  "format": "web",
  "width": 1024,
  "height": 1024,
  "url": "/uploads/images/uuid.png",
  "upscaled_url": null,
  "cost_raits": 20,
  "created_at": "..."
}
```

### POST /images/{image_id}/upscale
```json
// Request
{ "scale": 4 }

// Response 202
{ "image_id": "uuid", "status": "processing" }
```

### GET /images?limit=10&offset=0
```json
// Response 200
{
  "images": [
    { "image_id": "uuid", "prompt": "...", "thumbnail_url": "...", "format": "web", "created_at": "..." }
  ],
  "pagination": { ... }
}
```

---

## 7. ПЛАТЕЖИ

### GET /payments/methods
```json
// Response 200
{
  "methods": [
    { "id": "yookassa", "name": "ЮKassa", "icon": "yookassa.svg" },
    { "id": "robokassa", "name": "Robokassa", "icon": "robokassa.svg" },
    { "id": "cloudpayments", "name": "CloudPayments", "icon": "cloudpayments.svg" },
    { "id": "tbank", "name": "Т-Банк", "icon": "tbank.svg" }
  ],
  "exchange_rate": 10,
  "min_amount_rub": 100
}
```

### POST /payments/create
```json
// Request
{
  "amount_rub": 500,
  "provider": "yookassa"
}

// Response 200
{
  "payment_id": "uuid",
  "payment_url": "https://yookassa.ru/...",
  "amount_rub": 500,
  "amount_raits": 5000,
  "expires_at": "..."
}
```

### GET /payments/{payment_id}/status
```json
// Response 200
{
  "payment_id": "uuid",
  "status": "completed",
  "amount_rub": 500,
  "amount_raits": 5000,
  "completed_at": "..."
}
```

### POST /payments/webhook/{provider}
Webhook от платёжной системы (без авторизации, валидация по подписи)

---

## 8. WEBSOCKET

### /ws/generation/{session_id}?token=...

**События:**
```json
{"event": "connected", "session_id": "uuid"}
{"event": "step_started", "step": 1, "step_name": "Анализ", "total_steps": 4}
{"event": "step_progress", "step": 1, "progress": 50}
{"event": "step_completed", "step": 1}
{"event": "completed", "result": "...", "cost_raits": 50}
{"event": "error", "code": "GENERATION_FAILED", "message": "..."}
```

### /ws/image/{image_id}?token=...

**События:**
```json
{"event": "connected", "image_id": "uuid"}
{"event": "processing", "progress": 30}
{"event": "completed", "url": "/uploads/images/uuid.png"}
{"event": "error", "code": "IMAGE_FAILED", "message": "..."}
```

---

## 9. КОДЫ ОШИБОК

### Аутентификация
| Код | HTTP | Описание |
|-----|------|----------|
| INVALID_CREDENTIALS | 401 | Неверный email/пароль |
| TOKEN_EXPIRED | 401 | Токен истёк |
| TOKEN_INVALID | 401 | Невалидный токен |
| EMAIL_EXISTS | 400 | Email занят |

### Генерация
| Код | HTTP | Описание |
|-----|------|----------|
| INSUFFICIENT_BALANCE | 402 | Недостаточно Райтов |
| TOOL_NOT_FOUND | 404 | Инструмент не найден |
| SESSION_NOT_FOUND | 404 | Сессия не найдена |
| GENERATION_FAILED | 500 | Ошибка генерации |
| PROVIDER_UNAVAILABLE | 503 | Провайдер недоступен |

### Платежи
| Код | HTTP | Описание |
|-----|------|----------|
| PAYMENT_NOT_FOUND | 404 | Платёж не найден |
| PAYMENT_FAILED | 400 | Платёж не прошёл |
| INVALID_AMOUNT | 400 | Неверная сумма |

### Изображения
| Код | HTTP | Описание |
|-----|------|----------|
| IMAGE_NOT_FOUND | 404 | Изображение не найдено |
| IMAGE_FAILED | 500 | Ошибка генерации |
| INVALID_FORMAT | 400 | Неверный формат |

---

## 10. ТИПЫ ДАННЫХ

```typescript
interface User {
  id: string
  email: string
  name: string | null
  provider: 'local' | 'google' | 'yandex'
  balance: number
  created_at: string
}

interface Tab {
  id: string
  name: string
  icon: string
  tools_count: number
}

interface Tool {
  id: string
  name: string
  description: string
  icon: string
  supports_modes: ('quick' | 'standard')[]
  estimated_cost: number
}

interface GenerationSession {
  session_id: string
  tool_id: string
  mode: 'quick' | 'standard'
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  input_data: Record<string, any>
  result: string | null
  provider_used: string
  tokens_used: number
  cost_raits: number
  created_at: string
  completed_at: string | null
}

interface GeneratedImage {
  image_id: string
  status: 'processing' | 'completed' | 'failed'
  prompt: string
  format: 'web' | 'banner' | 'print' | 'messenger'
  width: number
  height: number
  url: string
  upscaled_url: string | null
  cost_raits: number
  created_at: string
}

interface Payment {
  payment_id: string
  status: 'pending' | 'completed' | 'failed'
  amount_rub: number
  amount_raits: number
  provider: string
  created_at: string
  completed_at: string | null
}

interface Transaction {
  id: string
  type: 'topup' | 'spend'
  amount: number
  description: string
  created_at: string
}
```

---

**Конец документа**
