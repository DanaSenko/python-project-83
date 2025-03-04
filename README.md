### Hexlet tests and linter status:
[![Actions Status](https://github.com/DanaSenko/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DanaSenko/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/7a79288aeba64220027b/maintainability)](https://codeclimate.com/github/DanaSenko/python-project-83/maintainability)
[![CI](https://github.com/DanaSenko/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/DanaSenko/python-project-83/actions/workflows/main.yml)

# Page Analyzer

Page Analyzer – это веб-приложение для анализа страниц, разработанное на Flask. Оно позволяет проверять страницы на доступность и извлекать метаинформацию.

## Демонстрация
Приложение доступно по ссылке: [Page Analyzer](https://python-project-83-0g5e.onrender.com)

## Установка и запуск

### 1. Клонирование репозитория
```sh
git clone https://github.com/yourusername/page_analyzer.git
cd page_analyzer
```

### 2. Установка зависимостей
```sh
make install
```

### 3. Создание базы данных
```sh
psql -d page_analyzer -f database/schema.sql
```

### 4. Запуск проекта
```sh
make start
```

После запуска сервер будет доступен по адресу `http://localhost:8000`.

## 📄 Функциональность
- Проверка доступности страниц
- Извлечение заголовков `h1`, `title`, `description`
- Сохранение истории проверок

## 🛠 Технологии
- Python
- Flask
- PostgreSQL
- Gunicorn



