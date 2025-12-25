# ТЕХНИЧЕСКОЕ ЗАДАНИЕ: Easy Writer Frontend (PWA)

**Версия:** 1.0  
**Дата:** Декабрь 2024  
**Тип:** React PWA (Progressive Web App)  
**Репозиторий:** easy-writer-frontend  
**Разработчик:** Middle+ / Senior-  
**Инструмент:** Cursor AI

---

## СОДЕРЖАНИЕ

1. [Общие сведения](#1-общие-сведения)
2. [Этап 1: Инициализация проекта](#этап-1-инициализация-проекта)
3. [Этап 2: Авторизация](#этап-2-авторизация)
4. [Этап 3: Личный кабинет](#этап-3-личный-кабинет)
5. [Этап 4: Табы и инструменты](#этап-4-табы-и-инструменты)
6. [Этап 5: Генерация контента](#этап-5-генерация-контента)
7. [Этап 6: Генерация изображений](#этап-6-генерация-изображений)
8. [Этап 7: Оплата и тарифы](#этап-7-оплата-и-тарифы)
9. [Этап 8: PWA функционал](#этап-8-pwa-функционал)
10. [Этап 9: Финальное тестирование](#этап-9-финальное-тестирование)

---

## 1. ОБЩИЕ СВЕДЕНИЯ

### 1.1 Назначение

Веб-приложение easy-writer.ru — AI-помощник для создания текстов и изображений.

### 1.2 Backend API

```
Production: https://api.easy-writer.ru/api/v1
Development: http://localhost:8000/api/v1
Документация: https://api.easy-writer.ru/docs
```

### 1.3 Стек технологий

| Технология | Версия | Назначение |
|------------|--------|------------|
| React | 18.x | UI фреймворк |
| TypeScript | 5.x | Типизация |
| Vite | 5.x | Сборка |
| TailwindCSS | 3.x | Стили |
| React Router | 6.x | Роутинг |
| TanStack Query | 5.x | Серверный стейт |
| Zustand | 4.x | Клиентский стейт |
| React Hook Form | 7.x | Формы |
| Zod | 3.x | Валидация |
| Axios | 1.x | HTTP клиент |

### 1.4 Структура проекта

```
easy-writer-frontend/
├── public/
│   ├── manifest.json
│   ├── sw.js
│   └── icons/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── auth.ts
│   │   ├── tools.ts
│   │   ├── generation.ts
│   │   ├── images.ts
│   │   ├── payments.ts
│   │   └── user.ts
│   ├── components/
│   │   ├── ui/
│   │   ├── auth/
│   │   ├── tools/
│   │   ├── generation/
│   │   ├── images/
│   │   ├── payments/
│   │   └── layout/
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── ToolPage.tsx
│   │   ├── HistoryPage.tsx
│   │   ├── ProfilePage.tsx
│   │   ├── BalancePage.tsx
│   │   └── PaymentPage.tsx
│   ├── hooks/
│   ├── store/
│   ├── types/
│   ├── utils/
│   ├── App.tsx
│   └── main.tsx
├── Dockerfile
├── nginx.conf
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### 1.5 Docker интеграция

```yaml
# Встраивается в easy-writer-network
Container: easy_writer_frontend
Image: nginx:alpine
Port: 3000 → 80
Domain: easy-writer.ru, www.easy-writer.ru
```

---

## ЭТАП 1: ИНИЦИАЛИЗАЦИЯ ПРОЕКТА

**Длительность:** 3 часа

### 1.1 Задачи

- [ ] Инициализировать Vite + React + TypeScript
- [ ] Настроить TailwindCSS
- [ ] Настроить ESLint + Prettier
- [ ] Создать структуру папок
- [ ] Настроить Axios клиент
- [ ] Создать Dockerfile и nginx.conf
- [ ] Настроить переменные окружения

### 1.2 Промпт для Cursor AI

```
Создай React PWA проект Easy Writer Frontend.

Требования:
1. Vite + React 18 + TypeScript 5
2. TailwindCSS с конфигом:
   - Тёмная тема (class strategy)
   - Кастомные цвета: primary, secondary, accent
   - Шрифт: Inter

3. Структура папок как в спецификации выше

4. Axios клиент (src/api/client.ts):
   - baseURL из env: VITE_API_URL
   - Interceptor: добавлять Authorization header
   - Interceptor: при 401 редирект на /login
   - Refresh token логика

5. Zustand store (src/store/authStore.ts):
   - user: User | null
   - accessToken: string | null
   - isAuthenticated: boolean
   - login(), logout(), setUser()

6. Dockerfile (multi-stage):
   - Build: node:20-alpine
   - Serve: nginx:alpine
   - Копировать nginx.conf

7. nginx.conf:
   - SPA fallback (try_files)
   - Gzip
   - Cache static assets
   - Proxy /api → backend (опционально)

8. .env.example:
   VITE_API_URL=https://api.easy-writer.ru/api/v1
   VITE_APP_NAME=Easy Writer

9. ESLint + Prettier конфиги

Не добавляй комментарии в код.
```

### 1.3 Тесты

**Тест 1 (Unit):** Сборка проекта
```bash
npm run build
```
Ожидание: сборка без ошибок, папка dist создана

**Тест 2 (Integration):** Docker build
```bash
docker build -t easy_writer_frontend .
docker run -p 3000:80 easy_writer_frontend
curl http://localhost:3000
```
Ожидание: HTML страница возвращается

**Тест 3 (Manual):** Открыть http://localhost:3000
Ожидание: страница загружается, нет ошибок в консоли

### 1.4 Критерии готовности

- [ ] `npm run dev` запускает dev сервер
- [ ] `npm run build` создаёт production сборку
- [ ] Docker образ собирается
- [ ] TailwindCSS работает
- [ ] Axios клиент настроен

---

## ЭТАП 2: АВТОРИЗАЦИЯ

**Длительность:** 6 часов

### 2.1 Задачи

- [ ] Страница регистрации
- [ ] Страница входа
- [ ] OAuth кнопки (Google, Yandex)
- [ ] Восстановление пароля
- [ ] Protected routes
- [ ] Хранение токенов

### 2.2 Страницы и компоненты

```
/login          → LoginPage
/register       → RegisterPage
/forgot-password → ForgotPasswordPage
/auth/callback  → OAuthCallbackPage (обработка OAuth)
```

### 2.3 Промпт для Cursor AI

```
Создай систему авторизации для Easy Writer Frontend.

API эндпоинты (backend уже реализован):
POST /auth/register — {email, password} → {user, access_token}
POST /auth/login — {email, password} → {user, access_token}
POST /auth/refresh — (cookie) → {access_token}
POST /auth/logout — выход
GET /auth/me — текущий пользователь
GET /auth/google — редирект на Google OAuth
GET /auth/yandex — редирект на Yandex OAuth

Требования:
1. Страницы:
   - LoginPage: форма email+password, кнопки OAuth, ссылка на регистрацию
   - RegisterPage: форма email+password+confirm, кнопки OAuth
   - ForgotPasswordPage: форма email
   - OAuthCallbackPage: обработка ?token=... из URL

2. Компоненты (src/components/auth/):
   - LoginForm.tsx
   - RegisterForm.tsx
   - OAuthButtons.tsx (Google + Yandex)
   - ForgotPasswordForm.tsx

3. Валидация (Zod):
   - email: valid email
   - password: min 8 символов
   - confirmPassword: совпадает с password

4. React Hook Form для форм

5. Хранение токенов:
   - access_token: Zustand store (память)
   - refresh_token: httpOnly cookie (ставит backend)

6. Protected Route компонент:
   - Если не авторизован → /login
   - Проверять isAuthenticated из store

7. API функции (src/api/auth.ts):
   - register(email, password)
   - login(email, password)
   - logout()
   - getMe()
   - refreshToken()

8. При старте приложения:
   - Вызвать refreshToken()
   - Если успех → getMe() → setUser()
   - Если ошибка → очистить store

9. UI:
   - Центрированные карточки форм
   - Индикатор загрузки на кнопках
   - Отображение ошибок под полями
   - Toast уведомления (успех/ошибка)

Не добавляй комментарии.
```

### 2.4 Тесты

**Тест 1 (Unit):** Валидация форм
```
1. Открыть /register
2. Ввести невалидный email
3. Проверить: ошибка валидации отображается
```

**Тест 2 (Integration):** Регистрация
```
1. Открыть /register
2. Заполнить форму валидными данными
3. Отправить
4. Проверить: редирект на /dashboard, пользователь в store
```

**Тест 3 (Manual):** OAuth flow
```
1. Открыть /login
2. Нажать "Войти через Google"
3. Авторизоваться в Google
4. Проверить: редирект на /dashboard
```

### 2.5 Критерии готовности

- [ ] Регистрация работает
- [ ] Логин работает
- [ ] OAuth Google работает
- [ ] OAuth Yandex работает
- [ ] Protected routes защищены
- [ ] Refresh token обновляет сессию

---

## ЭТАП 3: ЛИЧНЫЙ КАБИНЕТ

**Длительность:** 5 часов

### 3.1 Задачи

- [ ] Страница профиля
- [ ] Страница баланса
- [ ] История операций
- [ ] Настройки аккаунта

### 3.2 Страницы

```
/profile    → ProfilePage (данные пользователя)
/balance    → BalancePage (баланс Райтов, история)
/settings   → SettingsPage (смена пароля, удаление аккаунта)
```

### 3.3 Промпт для Cursor AI

```
Создай личный кабинет для Easy Writer Frontend.

API эндпоинты:
GET /user/profile — профиль пользователя
PUT /user/profile — обновление профиля
GET /user/balance — баланс и история
GET /user/transactions — история транзакций (пагинация)
PUT /user/password — смена пароля
DELETE /user/account — удаление аккаунта

Требования:
1. ProfilePage:
   - Аватар (инициалы или загрузка)
   - Email (readonly)
   - Имя (редактируемое)
   - Дата регистрации
   - Способ входа (email/Google/Yandex)
   - Кнопка "Сохранить"

2. BalancePage:
   - Текущий баланс в Райтах (крупно)
   - Кнопка "Пополнить"
   - График расходов за месяц (опционально)
   - Таблица транзакций:
     - Дата
     - Тип (пополнение/списание)
     - Сумма
     - Описание (инструмент)
   - Пагинация

3. SettingsPage:
   - Форма смены пароля (старый, новый, подтверждение)
   - Переключатель тёмной темы
   - Удаление аккаунта (с подтверждением)

4. Компоненты:
   - UserAvatar.tsx
   - BalanceCard.tsx
   - TransactionTable.tsx
   - TransactionRow.tsx
   - ChangePasswordForm.tsx

5. Типы (src/types/user.ts):
   interface User {
     id: string
     email: string
     name: string | null
     provider: 'local' | 'google' | 'yandex'
     balance: number
     created_at: string
   }
   
   interface Transaction {
     id: string
     type: 'topup' | 'spend'
     amount: number
     description: string
     created_at: string
   }

Не добавляй комментарии.
```

### 3.4 Тесты

**Тест 1 (Unit):** Отображение баланса
```
1. Залогиниться
2. Открыть /balance
3. Проверить: баланс отображается
```

**Тест 2 (Integration):** Обновление профиля
```
1. Открыть /profile
2. Изменить имя
3. Сохранить
4. Обновить страницу
5. Проверить: имя сохранилось
```

**Тест 3 (Manual):** История транзакций
```
1. Открыть /balance
2. Пролистать таблицу
3. Проверить пагинацию
```

### 3.5 Критерии готовности

- [ ] Профиль отображается и редактируется
- [ ] Баланс отображается
- [ ] История транзакций с пагинацией
- [ ] Смена пароля работает
- [ ] Тёмная тема переключается

---

## ЭТАП 4: ТАБЫ И ИНСТРУМЕНТЫ

**Длительность:** 6 часов

### 4.1 Задачи

- [ ] Dashboard с табами
- [ ] Сетка инструментов
- [ ] Страница инструмента
- [ ] Динамические формы

### 4.2 Структура табов (MVP)

```
everyday   — На каждый день (8 инструментов)
education  — Обучение (8 инструментов)
business   — Бизнес (6 инструментов)
marketing  — Маркетинг (7 инструментов)
special    — Особый случай (6 инструментов)
```

### 4.3 Страницы

```
/dashboard          → DashboardPage (табы + инструменты)
/tool/:toolId       → ToolPage (форма инструмента)
```

### 4.4 Промпт для Cursor AI

```
Создай систему табов и инструментов для Easy Writer Frontend.

API эндпоинты:
GET /tools/tabs — список табов
GET /tools/tabs/{tab_id} — инструменты таба
GET /tools/{tool_id}/schema — JSON Schema формы инструмента

Требования:
1. DashboardPage:
   - Горизонтальные табы (скролл на мобильном)
   - Сетка инструментов выбранного таба
   - Поиск по инструментам (фильтрация)
   - Сохранение выбранного таба в URL (?tab=everyday)

2. Компонент TabsNavigation:
   - Иконка + название таба
   - Активный таб выделен
   - Анимация переключения

3. Компонент ToolGrid:
   - Карточки 3 в ряд (desktop), 2 (tablet), 1 (mobile)
   - Ленивая загрузка изображений

4. Компонент ToolCard:
   - Иконка
   - Название
   - Краткое описание
   - Бейдж режимов (quick/standard)
   - Hover эффект
   - Клик → /tool/{toolId}

5. ToolPage:
   - Название и описание инструмента
   - Динамическая форма из JSON Schema
   - Выбор режима (quick/standard) если поддерживается
   - Кнопка "Сгенерировать"
   - Стоимость в Райтах (примерная)

6. Компонент DynamicForm:
   - Генерация полей из JSON Schema
   - Поддержка типов: string, text, number, select, checkbox
   - Валидация из schema (required, minLength, maxLength)

7. Типы:
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

8. Кеширование:
   - Список табов — staleTime: 1 час
   - Инструменты таба — staleTime: 30 минут

Не добавляй комментарии.
```

### 4.5 Тесты

**Тест 1 (Unit):** Переключение табов
```
1. Открыть /dashboard
2. Кликнуть на таб "Бизнес"
3. Проверить: URL изменился на ?tab=business
4. Проверить: отображаются инструменты бизнеса
```

**Тест 2 (Integration):** Открытие инструмента
```
1. Кликнуть на карточку инструмента
2. Проверить: открылась страница /tool/{id}
3. Проверить: форма отрисовалась
```

**Тест 3 (Manual):** Мобильная версия
```
1. Открыть в мобильном режиме (DevTools)
2. Проверить: табы скроллятся
3. Проверить: карточки в 1 колонку
```

### 4.6 Критерии готовности

- [ ] Все 5 табов отображаются
- [ ] Инструменты загружаются
- [ ] Динамические формы работают
- [ ] Адаптивная вёрстка

---

## ЭТАП 5: ГЕНЕРАЦИЯ КОНТЕНТА

**Длительность:** 8 часов

### 5.1 Задачи

- [ ] Отправка запроса на генерацию
- [ ] Quick режим (синхронный)
- [ ] Standard режим (WebSocket)
- [ ] Отображение результата
- [ ] История генераций

### 5.2 Промпт для Cursor AI

```
Создай систему генерации контента для Easy Writer Frontend.

API эндпоинты:
POST /tools/{tool_id}/execute — запуск генерации
GET /generation/sessions/{id} — получение результата
GET /generation/sessions — история (пагинация)
DELETE /generation/sessions/{id} — удаление
WebSocket: /ws/generation/{session_id} — прогресс standard режима

Требования:
1. Quick режим:
   - POST запрос
   - Показать спиннер
   - Получить результат сразу в response
   - Отобразить результат

2. Standard режим:
   - POST запрос → получить session_id
   - Подключиться к WebSocket
   - Отображать прогресс по шагам:
     - Шаг 1: Анализ задачи
     - Шаг 2: Генерация структуры
     - Шаг 3: Генерация контента
     - Шаг 4: Редактура
   - При событии "completed" показать результат

3. Компонент GenerationProgress:
   - Список шагов с иконками
   - Текущий шаг выделен + спиннер
   - Завершённые шаги — галочка
   - Процент общего прогресса

4. Компонент ResultDisplay:
   - Текстовый результат с форматированием (Markdown)
   - Кнопка "Копировать"
   - Кнопка "Скачать" (txt/docx)
   - Кнопка "Сгенерировать заново"
   - Использовано Райтов

5. Страница HistoryPage (/history):
   - Таблица генераций
   - Колонки: дата, инструмент, превью, статус, Райты
   - Клик → открыть результат
   - Удаление

6. Обработка ошибок:
   - Недостаточно Райтов → предложить пополнить
   - Ошибка генерации → показать сообщение + retry
   - WebSocket disconnect → переподключение (3 попытки)

7. Хук useGeneration:
   - executeQuick(toolId, input)
   - executeStandard(toolId, input)
   - progress, result, error, isLoading

8. Хук useWebSocket:
   - connect(url)
   - disconnect()
   - onMessage callback
   - reconnect логика

Не добавляй комментарии.
```

### 5.3 Тесты

**Тест 1 (Unit):** Quick генерация
```
1. Открыть инструмент "Проверка орфографии"
2. Ввести текст с ошибками
3. Нажать "Сгенерировать"
4. Проверить: результат отображается
```

**Тест 2 (Integration):** Standard генерация
```
1. Открыть инструмент с поддержкой standard
2. Заполнить форму
3. Выбрать режим "Стандартный"
4. Нажать "Сгенерировать"
5. Проверить: прогресс отображается по шагам
6. Проверить: результат появляется в конце
```

**Тест 3 (Manual):** Копирование результата
```
1. Сгенерировать текст
2. Нажать "Копировать"
3. Вставить в блокнот
4. Проверить: текст скопировался
```

### 5.4 Критерии готовности

- [ ] Quick режим работает
- [ ] Standard режим с WebSocket
- [ ] Прогресс отображается
- [ ] Результат форматируется (Markdown)
- [ ] Копирование работает
- [ ] История генераций

---

## ЭТАП 6: ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЙ

**Длительность:** 5 часов

### 6.1 Задачи

- [ ] Форма генерации изображения
- [ ] Выбор формата (web, banner, print, messenger)
- [ ] Отображение результата
- [ ] Апскейл изображения
- [ ] Скачивание

### 6.2 Промпт для Cursor AI

```
Создай систему генерации изображений для Easy Writer Frontend.

API эндпоинты:
POST /images/generate — генерация
GET /images/{id} — получение
POST /images/{id}/upscale — апскейл
GET /images — список изображений пользователя
WebSocket: /ws/image/{image_id} — прогресс

Форматы:
- web: 1024x1024 (для сайтов)
- banner: 2048x1024 (баннеры)
- print: 2048x2048 (для печати)
- messenger: 512x512 (соцсети)

Требования:
1. Инструмент "Генерация изображения" (special таб):
   - Поле промпта (textarea)
   - Выбор формата (radio или select)
   - Выбор стиля (опционально): реализм, иллюстрация, арт
   - Кнопка "Сгенерировать"
   - Превью размера

2. Инструмент "Поздравительная открытка":
   - Выбор повода (день рождения, свадьба, и т.д.)
   - Имя получателя
   - Стиль (весёлый, официальный)
   - Результат: текст + изображение

3. Компонент ImageGenerator:
   - Форма ввода
   - Прогресс генерации (спиннер + процент)
   - Результат — изображение

4. Компонент ImageResult:
   - Изображение (масштабируемое)
   - Кнопки: Скачать, Апскейл, Сгенерировать заново
   - Информация: размер, формат

5. Компонент ImageUpscaler:
   - Выбор масштаба: 2x, 4x
   - Предупреждение о стоимости
   - Прогресс
   - Результат

6. Страница /images (галерея):
   - Сетка изображений пользователя
   - Фильтр по формату
   - Клик → модальное окно с действиями
   - Удаление

7. Скачивание:
   - Формат: PNG
   - Имя файла: easy-writer-{timestamp}.png

Не добавляй комментарии.
```

### 6.3 Тесты

**Тест 1 (Unit):** Выбор формата
```
1. Открыть генерацию изображений
2. Выбрать формат "banner"
3. Проверить: превью размера обновилось
```

**Тест 2 (Integration):** Генерация изображения
```
1. Ввести промпт
2. Выбрать формат
3. Нажать "Сгенерировать"
4. Проверить: изображение появилось
```

**Тест 3 (Manual):** Скачивание
```
1. Сгенерировать изображение
2. Нажать "Скачать"
3. Проверить: файл скачался
```

### 6.4 Критерии готовности

- [ ] Генерация изображений работает
- [ ] Все форматы поддерживаются
- [ ] Апскейл работает
- [ ] Скачивание работает
- [ ] Галерея отображается

---

## ЭТАП 7: ОПЛАТА И ТАРИФЫ

**Длительность:** 6 часов

### 7.1 Задачи

- [ ] Страница пополнения баланса
- [ ] Интеграция виджетов оплаты
- [ ] Страница тарифов (опционально)
- [ ] Обработка webhook (информирование)

### 7.2 Платёжные системы

| Система | Виджет |
|---------|--------|
| ЮKassa | yookassa-checkout-widget |
| Robokassa | iframe |
| CloudPayments | cp-widget |
| Т-Банк | tinkoff-widget |

### 7.3 Промпт для Cursor AI

```
Создай систему оплаты для Easy Writer Frontend.

API эндпоинты:
POST /payments/create — создать платёж → {payment_url, payment_id}
GET /payments/{id}/status — статус платёжа
GET /payments/methods — доступные методы оплаты

Требования:
1. Страница PaymentPage (/payment):
   - Текущий баланс
   - Выбор суммы пополнения:
     - Предустановленные: 100, 300, 500, 1000 руб
     - Кастомная сумма (input)
   - Конвертация в Райты (курс с backend)
   - Выбор платёжной системы
   - Кнопка "Оплатить"

2. Компонент PaymentMethodSelector:
   - Карточки платёжных систем
   - Иконки
   - Выбор одного

3. Компонент AmountSelector:
   - Кнопки быстрого выбора
   - Input для кастомной суммы
   - Отображение итога в Райтах

4. Flow оплаты:
   a) Пользователь выбирает сумму и метод
   b) POST /payments/create → получить payment_url
   c) Редирект на payment_url или открытие виджета
   d) После оплаты → редирект на /payment/success?payment_id=...
   e) Страница успеха проверяет статус и обновляет баланс

5. Страница PaymentSuccessPage:
   - Проверка статуса платежа (polling 3 сек)
   - Успех: "Баланс пополнен на X Райтов"
   - Ошибка: "Платёж не прошёл"
   - Кнопка "Вернуться в кабинет"

6. Страница PaymentFailPage:
   - Сообщение об ошибке
   - Кнопка "Попробовать снова"

7. Компонент BalanceWidget (в header):
   - Текущий баланс
   - Клик → /payment

8. Обновление баланса:
   - После успешной оплаты
   - После генерации (списание)
   - Периодически (каждые 5 минут)

Не добавляй комментарии.
```

### 7.4 Тесты

**Тест 1 (Unit):** Выбор суммы
```
1. Открыть /payment
2. Выбрать 300 руб
3. Проверить: отображается конвертация в Райты
```

**Тест 2 (Integration):** Создание платежа
```
1. Выбрать сумму и метод
2. Нажать "Оплатить"
3. Проверить: редирект на платёжную систему
```

**Тест 3 (Manual):** Тестовый платёж
```
1. Использовать тестовые данные ЮKassa
2. Провести платёж
3. Проверить: баланс обновился
```

### 7.5 Критерии готовности

- [ ] Выбор суммы работает
- [ ] Выбор платёжной системы
- [ ] Редирект на оплату
- [ ] Обработка успеха/ошибки
- [ ] Баланс обновляется

---

## ЭТАП 8: PWA ФУНКЦИОНАЛ

**Длительность:** 4 часа

### 8.1 Задачи

- [ ] Manifest.json
- [ ] Service Worker
- [ ] Офлайн страница
- [ ] Установка на устройство
- [ ] Push уведомления (опционально)

### 8.2 Промпт для Cursor AI

```
Настрой PWA функционал для Easy Writer Frontend.

Требования:
1. manifest.json:
   - name: "Easy Writer"
   - short_name: "EasyWriter"
   - description: "AI-помощник для создания текстов"
   - theme_color: #6366f1 (indigo)
   - background_color: #ffffff
   - display: standalone
   - orientation: portrait-primary
   - icons: 192x192, 512x512 (PNG)
   - start_url: /dashboard
   - scope: /

2. Service Worker (Workbox):
   - Кеширование статики (CSS, JS, шрифты)
   - Network-first для API
   - Офлайн fallback страница

3. Офлайн страница (offline.html):
   - Сообщение "Нет подключения к интернету"
   - Кнопка "Повторить"
   - Сохранённый баланс (из localStorage)

4. Компонент InstallPrompt:
   - Показывать предложение установить
   - Кнопки "Установить" / "Позже"
   - Сохранять отказ в localStorage (не показывать 7 дней)

5. Компонент UpdatePrompt:
   - При обновлении SW показать уведомление
   - Кнопка "Обновить"

6. Vite PWA плагин:
   - vite-plugin-pwa
   - Автогенерация SW
   - Inject manifest

7. Иконки:
   - Создать из логотипа
   - Размеры: 72, 96, 128, 144, 152, 192, 384, 512

Не добавляй комментарии.
```

### 8.3 Тесты

**Тест 1 (Unit):** Manifest загружается
```
1. Открыть DevTools → Application → Manifest
2. Проверить: manifest отображается корректно
```

**Тест 2 (Integration):** Service Worker
```
1. DevTools → Application → Service Workers
2. Проверить: SW активен
3. Включить офлайн режим
4. Обновить страницу
5. Проверить: офлайн страница отображается
```

**Тест 3 (Manual):** Установка
```
1. Открыть на мобильном (Android Chrome)
2. Дождаться предложения установить
3. Установить
4. Открыть с домашнего экрана
5. Проверить: работает как приложение
```

### 8.4 Критерии готовности

- [ ] Manifest валиден (Lighthouse)
- [ ] Service Worker работает
- [ ] Офлайн страница показывается
- [ ] Установка работает
- [ ] Lighthouse PWA score > 90

---

## ЭТАП 9: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ

**Длительность:** 4 часа

### 9.1 Задачи

- [ ] E2E тесты (Playwright)
- [ ] Lighthouse аудит
- [ ] Кроссбраузерное тестирование
- [ ] Мобильное тестирование
- [ ] Деплой

### 9.2 Промпт для Cursor AI

```
Создай E2E тесты и настрой деплой для Easy Writer Frontend.

Требования:
1. Playwright тесты (tests/e2e/):
   - auth.spec.ts: регистрация, логин, logout
   - generation.spec.ts: quick генерация
   - payment.spec.ts: открытие страницы оплаты
   - navigation.spec.ts: переходы между страницами

2. Конфиг playwright.config.ts:
   - Браузеры: chromium, firefox, webkit
   - Mobile viewports
   - Screenshots on failure
   - Video on failure

3. package.json scripts:
   - test:e2e — запуск Playwright
   - test:e2e:ui — с UI режимом
   - lighthouse — запуск аудита

4. GitHub Actions (.github/workflows/frontend.yml):
   - Trigger: push, PR
   - Jobs: lint, build, e2e
   - Deploy: только main ветка
   - Deploy target: сервер через SSH

5. Deploy скрипт (scripts/deploy.sh):
   - Build
   - Copy to server via rsync
   - Restart nginx

6. Чеклист перед релизом:
   - [ ] Lighthouse Performance > 80
   - [ ] Lighthouse Accessibility > 90
   - [ ] Lighthouse Best Practices > 90
   - [ ] Lighthouse SEO > 90
   - [ ] Lighthouse PWA > 90
   - [ ] Нет ошибок в консоли
   - [ ] Работает на Chrome, Firefox, Safari
   - [ ] Работает на iOS Safari, Android Chrome

Не добавляй комментарии.
```

### 9.3 Тесты

**Тест 1 (E2E):** Полный flow
```bash
npx playwright test
```
Ожидание: все тесты проходят

**Тест 2 (Lighthouse):** Аудит
```bash
npx lighthouse https://easy-writer.ru --output=html
```
Ожидание: все метрики > 80

**Тест 3 (Manual):** Кроссбраузерность
```
1. Открыть в Chrome, Firefox, Safari
2. Проверить основные функции
3. Проверить на мобильных устройствах
```

### 9.4 Критерии готовности

- [ ] E2E тесты проходят
- [ ] Lighthouse > 80 по всем метрикам
- [ ] Работает в основных браузерах
- [ ] Работает на мобильных
- [ ] Деплой настроен

---

## ЧЕКЛИСТ ЗАВЕРШЕНИЯ

### Функционал
- [ ] Регистрация и авторизация
- [ ] OAuth (Google, Yandex)
- [ ] Личный кабинет
- [ ] 5 табов с инструментами
- [ ] Quick и Standard генерация
- [ ] WebSocket прогресс
- [ ] Генерация изображений
- [ ] Оплата (4 платёжные системы)
- [ ] PWA (установка, офлайн)

### Качество
- [ ] TypeScript без ошибок
- [ ] ESLint без warnings
- [ ] E2E тесты проходят
- [ ] Lighthouse > 80
- [ ] Адаптивная вёрстка
- [ ] Тёмная тема

### Инфраструктура
- [ ] Docker образ собирается
- [ ] CI/CD настроен
- [ ] Production деплой

---

**Конец документа**

**Версия:** 1.0  
**Дата:** Декабрь 2024
