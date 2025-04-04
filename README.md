# API Documentation

## Содержание
- [Обзор](#обзор)
- [Особенности](#особенности)
- [Установка](#установка)
- [Использование](#использование)
- [Дерево проекта](#дерево-проекта)
- [API Endpoints](#api-endpoints)
- [Схема базы данных](#cхема-базы-данных)
- [Обзор тестов](#обзор-тестов)
- [Результаты тестов](#результаты-тестов)
- [Лицензия](#лицензия)

## Обзор
Это приложение FastAPI, которое предоставляет сервис сокращения ссылок. Пользователи могут создавать короткие ссылки, которые перенаправляют на оригинальные URL, управлять своими ссылками и отслеживать статистику использования.

## Особенности
- Создание коротких ссылок
- Перенаправление на оригинальные URL
- Регистрация и аутентификация пользователей
- Управление сроком действия ссылок
- Статистика использования

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/NasPozd/API-link-shortening-service.git
   cd API-link-shortening-service
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите приложение:
   ```bash
   uvicorn app.main:app
   ```

## Использование
- **Создать ссылку**: POST `/links/`
- **Получить статистику ссылки**: GET `/links/{short_code}/stats`
- **Регистрация пользователя**: POST `/users/`
- **Вход пользователя**: POST `/users/login`

## Дерево проекта
```
API-link-shortening-service/
├── app/
│   ├── core/
│   │   ├── config.py - Конфигурация приложения
│   │   ├── security.py - Логика безопасности
│   ├── db/
│   │   ├── database.py - Логика подключения к базе данных
│   ├── models/
│   │   ├── link.py - Модель данных для ссылок
│   │   ├── project.py - Модель данных для проектов
│   │   ├── user.py - Модель данных для пользователей
│   ├── routers/
│   │   ├── links.py - Определения маршрутов для ссылок
│   │   ├── stats.py - Определения маршрутов для статистики
│   │   ├── users.py - Определения маршрутов для управления пользователями
│   ├── schemas/
│   │   ├── link.py - Схемы валидации для ссылок
│   │   ├── user.py - Схемы валидации для пользователей
│   ├── utils/
│   │   ├── cache.py - Утилиты для кэширования
│   │   ├── short_code.py - Утилиты для генерации коротких кодов
│   │   ├── valid_url.py - Утилиты для валидации URL
│   ├── main.py - Главная точка входа для приложения FastAPI
├── tests/
│   ├── api/
│   │   ├── test_auth_api.py - Тесты для аутентификации
│   │   ├── test_links_api.py - Тесты для ссылок
│   ├── unit/
│   │   ├── test_link_generation.py - Модульные тесты для генерации ссылок
│   │   ├── test_link_model.py - Модульные тесты для модели ссылок
│   │   ├── test_user_model.py - Модульные тесты для модели пользователей
│   ├── integration/
│   │   ├── test_auth_flow.py - Интеграционные тесты для аутентификации
│   │   ├── test_db_integration.py - Интеграционные тесты для базы данных
├── logs.html - Логи результатов тестов
├── requirements.txt - Зависимости проекта
├── README.md - Документация проекта
```

## API Endpoints
### Ссылки
1. **Создать ссылку**
   - **POST /links/**
   - **Тело запроса**: 
     ```json
     {
       "original_url": "https://example.com",
       "custom_alias": "example",
       "expires_at": "2025-01-01T00:00:00Z"
     }
     ```
   - **Ответ**:
     ```json
     {
       "id": 1,
       "original_url": "https://example.com",
       "short_code": "abc123",
       "created_at": "2023-01-01T00:00:00Z",
       "expires_at": "2025-01-01T00:00:00Z",
       "clicks": 0,
       "last_accessed": "2023-01-01T00:00:00Z",
       "user_id": null
     }
     ```

2. **Поиск ссылки**
   - **GET /links/search?original_url=https://example.com**
   - **Ответ**:
     ```json
     {
       "id": 1,
       "original_url": "https://example.com",
       "short_code": "abc123",
       "created_at": "2023-01-01T00:00:00Z",
       "expires_at": "2025-01-01T00:00:00Z",
       "clicks": 0,
       "last_accessed": "2023-01-01T00:00:00Z",
       "user_id": null
     }
     ```

3. **Получить истекшие ссылки**
   - **GET /links/expired**
   - **Ответ**: Список истекших ссылок в том же формате, что и ответ на создание ссылки.

4. **Удалить неиспользуемые ссылки**
   - **DELETE /links/unused?days=30**
   - **Ответ**: Список удаленных ссылок в том же формате, что и ответ на создание ссылки.

5. **Обновить ссылку**
   - **PUT /links/{short_code}**
   - **Тело запроса**: 
     ```json
     {
       "original_url": "https://newexample.com",
       "expires_at": "2025-01-01T00:00:00Z"
     }
     ```
   - **Ответ**: Обновленная ссылка в том же формате, что и ответ на создание ссылки.

6. **Удалить ссылку**
   - **DELETE /links/{short_code}**
   - **Ответ**: Нет содержимого (204).

7. **Перенаправить ссылку**
   - **GET /links/{short_code}**
   - **Ответ**: Перенаправляет на оригинальный URL.

### Статистика
1. **Получить статистику ссылки**
   - **GET /links/{short_code}/stats**
   - **Ответ**:
     ```json
     {
       "original_url": "https://example.com",
       "created_at": "2023-01-01T00:00:00Z",
       "clicks": 0,
       "last_accessed": "2023-01-01T00:00:00Z"
     }
     ```

### Пользователи
1. **Создать пользователя**
   - **POST /users/**
   - **Тело запроса**: 
     ```json
     {
       "username": "newuser",
       "password": "password123"
     }
     ```
   - **Ответ**:
     ```json
     {
       "username": "newuser",
       "password": "password123"
     }
     ```

2. **Вход пользователя**
   - **POST /users/login**
   - **Тело запроса**: 
     ```json
     {
       "username": "newuser",
       "password": "password123"
     }
     ```
   - **Ответ**:
     ```json
     {
       "access_token": "jwt_token",
       "token_type": "bearer"
     }
     ```

## Схема базы данных

### Таблицы и их структура:

#### Таблица `links`
- **id**: Integer, primary key
- **original_url**: String (до 2048 символов), не может быть пустым
- **short_code**: String, уникальный
- **created_at**: DateTime, по умолчанию текущее время UTC
- **expires_at**: DateTime, может быть пустым
- **clicks**: Integer, по умолчанию 0
- **last_accessed**: DateTime, может быть пустым
- **user_id**: Integer, внешний ключ, ссылающийся на `users.id`, может быть пустым

#### Таблица `users`
- **id**: Integer, primary key
- **username**: String, уникальный, индексированный
- **hashed_password**: String

#### Таблица `projects`
- **id**: Integer, primary key
- **name**: String, не может быть пустым
- **links**: Связь с моделью `Link`, позволяющая доступ к связанным ссылкам.

| Таблица    | Поле             | Тип         | Ограничения                          |
|------------|------------------|-------------|--------------------------------------|
| **users**  | `id`             | Integer     | Primary Key                          |
|            | `username`       | String      | Unique, Indexed                      |
|            | `hashed_password`| String      |                                      |
| **links**  | `id`             | Integer     | Primary Key                          |
|            | `original_url`   | String(2048)| Not Null                             |
|            | `short_code`     | String      | Unique                               |
|            | `created_at`     | DateTime    | Default: текущее время              |
|            | `expires_at`     | DateTime    | Nullable                             |
|            | `clicks`         | Integer     | Default: 0                          |
|            | `last_accessed`  | DateTime    | Nullable                             |
|            | `user_id`        | Integer     | ForeignKey("users.id"), Nullable     |
|            | `project_id`     | Integer     | ForeignKey("projects.id"), Nullable  |
| **projects**| `id`            | Integer     | Primary Key                          |
|            | `name`           | String      | Not Null                             |

#### Связи:
- **users → links**  
  Один пользователь может иметь множество ссылок (`user_id` в `links`).
- **projects → links**  
  Один проект может содержать множество ссылок (`project_id` в `links`).

#### Индексы:
- `username` (users) — уникальный.
- `short_code` (links) — уникальный.

![](https://raw.githubusercontent.com/NasPozd/API-link-shortening-service/refs/heads/main/docs/db_schema.png)

## Обзор тестов
В этом проекте представлен комплексный набор тестов для обеспечения функциональности и надежности сервиса сокращения ссылок API. Ниже приведено подробное описание тестов, реализованных в проекте.

### Модульные тесты
- **test_user_creation**: 
  - **Вход**: Имя пользователя и пароль.
  - **Выход**: Успешное создание пользователя с хэшированным паролем.
  
- **test_password_hashing**: 
  - **Вход**: Оригинальный пароль.
  - **Выход**: Хэшированный пароль, который можно проверить.

- **test_short_code_uniqueness**: 
  - **Вход**: Существующий короткий код.
  - **Выход**: Новый короткий код, который не совпадает с существующим.

- **test_short_code_generation_without_input**: 
  - **Вход**: Нет входных данных.
  - **Выход**: Сгенерированный короткий код длиной 6 символов.

- **test_link_create_validation**: 
  - **Вход**: Данные для создания ссылки (оригинальный URL и дата истечения).
  - **Выход**: Успешное создание экземпляра схемы `LinkCreate`.

- **test_invalid_url**: 
  - **Вход**: Недопустимый URL.
  - **Выход**: `ValidationError`.

- **test_link_expiration**: 
  - **Вход**: Ссылка с установленной датой истечения.
  - **Выход**: Правильное определение, истекла ли ссылка.

### Интеграционные тесты
- **test_link_lifecycle**: 
  - **Вход**: Данные для создания ссылки.
  - **Выход**: Успешное создание, извлечение и удаление ссылки из базы данных.

- **test_full_auth_flow**: 
  - **Вход**: Данные для регистрации и входа пользователя.
  - **Выход**: Успешная регистрация, вход и создание ссылки.

- **test_link_stats**: 
  - **Вход**: Ссылка.
  - **Выход**: Статистика кликов для ссылки.

### API тесты
- **test_create_link**: 
  - **Вход**: Оригинальный URL.
  - **Выход**: Успешное создание ссылки с коротким кодом.

- **test_create_link_invalid_url**: 
  - **Вход**: Недопустимый URL.
  - **Выход**: Статус 422 Unprocessable Entity.

- **test_get_link_stats**: 
  - **Вход**: Короткий код ссылки.
  - **Выход**: Статистика для созданной ссылки.

- **test_update_link**: 
  - **Вход**: Новый оригинальный URL для существующей ссылки.
  - **Выход**: Успешное обновление ссылки.

- **test_delete_link**: 
  - **Вход**: Короткий код ссылки.
  - **Выход**: Успешное удаление ссылки.

- **test_create_and_retrieve_link**: 
  - **Вход**: Оригинальный URL.
  - **Выход**: Успешное создание и извлечение статистики ссылки.

## Результаты тестов
Все 19 тестов прошли успешно. С логами запуска контейнеров и результатами тестов можно ознакомиться в файле [здесь](https://naspozd.github.io/API-link-shortening-service/logs.html).
