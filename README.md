# BILLING - Yookassa

## Описание


## Стек
  FastAPI, aiohttp, SQLAlchemy, Pytest, gunicorn, nginx, alembic, Postgres, apscheduler

## Запуск
  - Заполняем .env (см. .env.template)
  - docker-compose up --build
  - Миграции см. ниже
  - тесты автоматом в docker-compose(deribit_tests)

## Миграции
  - Инит миграции через алембик(алембик подкручен - зависит от .env)
  - доп. миграции, если необходимо, то из папки deribit_api:
    - alembic revision -m "migration2" --autogenerate
    - alembic upgrade head

## URL
  - http://127.0.0.1/deribit/api/openapi - документация

 


