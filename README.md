# FastAPI Blog Platform 🚀

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-orange)](https://sqlalchemy.org)


Пример классического APP на FastAPI с полной аутентификацией, авторизацией и управлением контентом. Построена на современном асинхронном стеке Python.

## ✨ Особенности

- **🔐 JWT Аутентификация** - безопасная система входа/регистрации
- **👥 Управление правами** - авторы управляют только своими постами
- **📝 CRUD операции** - полное управление постами
- **📄 Пагинация и фильтрация** - эффективная работа с большими данными
- **⚡ Асинхронный API** - высокая производительность
- **📚 Автодокументация** - Swagger UI

## 🛠 Технологический стек

- **Framework**: FastAPI
- **Database**: PostgreSQL с SQLAlchemy 2.0
- **Authentication**: JWT tokens
- **Password hashing**: bcrypt
- **Validation**: Pydantic v2
- **Async**: asyncpg, асинхронные эндпоинты

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- PostgreSQL 13+
- pip

### Установка

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/yourusername/fastapi-blog-platform
cd fastapi-blog-platform
```

2. **Создайте и активируйте виртуальное окружение**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Запуск uvicorn**
```bash
uvicorn app.main:app --reload
http://127.0.0.1:8000/api/openapi/
```

5. **Пример .env**
```bash
SECRET_KEY=yoursecretkey
ALGORITHM=HS256
```