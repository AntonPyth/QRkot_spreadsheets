# 😻 QRKot_spreadsheets — Благотворительный фонд поддержки котиков с возможностью выгрузки отчетов

## 📖 Описание проекта
**QRKot_spreadsheets** — это сервис для пожертвований в фонд поддержки котиков.

🔑 Основные возможности:
- Регистрация и аутентификация пользователей;
- Создание и просмотр благотворительных проектов;
- Возможность делать пожертвования в активные проекты;
- Автоматическое распределение средств между проектами;
- Просмотр собственных пожертвований;
- Администрирование доступно только суперпользователю.
- Выгрузка отчетов на Google Cloud в формате электронных таблиц google_sheets

## 📂 Структура проекта
```
cat_charity_fund:
  ├── alembic
       ├── versions
       ├── env.py
       ├── script.py.mako
  ├── app
       ├── api
            ├── endpoints
                ├── __init__.py
                ├── apis_google.py
                ├── charity_project.py
                ├── donation.py
                ├── user.py
            ├── __init__.py
            ├── routers.py
            ├── validators.py
       ├── core
            ├── __init__.py
            ├── base.py
            ├── config.py
            ├── db.py
            ├── google_client.py
            ├── init_db.py
            ├── user.py
       ├── crud
            ├── __init__.py
            ├── base.py
            ├── charity_project.py
            ├── donation.py
       ├── models
            ├── __init__.py
            ├── charity_project.py
            ├── donation_base.py
            ├── donation.py
            ├── user.py
       ├── schemas
            ├── __init__.py
            ├── charity_project.py
            ├── donation.py
            ├── user.py
       ├── services
            ├── __init__.py
            ├── apis_google.py
            ├── services.py
       ├── __init__.py
       ├── main.py
  ├── postman_collection
  ├── tests
  ├── venv
  ├── .env
  ├── .flake8
  ├── .gitignore
  ├── alembic.ini
  ├── openapi.json
  ├── pytest.ini
  ├── README.md
  ├── requirements.txt
  └── setup_for_postman.py
```

## 🚀 Запуск проекта
1. Клонировать репозиторий:
```bash
git clone git@github.com:AntonPyth/cat_charity_fund.git
```
2. Создать и активировать виртуальное окружение:

Для Linux/macOS:
```
python3 -m venv venv
source venv/bin/activate
```
Для Windows:
```
python -m venv venv
. venv\Scripts\activate
```
3. Обновить pip и установить зависимости из ```requirements.txt```
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Запустить проект:
```bash
uvicorn app.main:app
```
После запуска проект будет доступен по адресу: http://127.0.0.1:8000/docs/

## 🛠 Используемые технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pydantic](https://img.shields.io/badge/pydantic-%23E92063.svg?style=for-the-badge&logo=pydantic&logoColor=white)

![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF4500?style=for-the-badge)

## 👤 Автор
[Кочуев Антон]  (https://github.com/AntonPyth)

## Environment variables
