### Hexlet tests and linter status:
[![Actions Status](https://github.com/DanaSenko/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DanaSenko/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/7a79288aeba64220027b/maintainability)](https://codeclimate.com/github/DanaSenko/python-project-83/maintainability)
[![CI](https://github.com/DanaSenko/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/DanaSenko/python-project-83/actions/workflows/main.yml)

# Page Analyzer

Page Analyzer – это веб-приложение для анализа страниц, разработанное на Flask. Оно позволяет проверять страницы на доступность и извлекать метаинформацию.

## Демонстрация
Приложение доступно по ссылке: [Page Analyzer](https://python-project-83-0g5e.onrender.com)

## Установка и запуск

### 1. Установка зависимостей
```sh
make install
```

### 2. Создание базы данных
```sh
psql -d <database_name> -f database.sql
```

### 3. Запуск проекта
```sh
make start
```

## Функциональность
- Проверка доступности страниц
- Извлечение заголовков `h1`, `title`, `description`
- Сохранение истории проверок

## 🛠 Технологии
- Python
- Flask
- PostgreSQL
- Gunicorn



