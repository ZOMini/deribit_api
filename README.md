# Deribit_API(Test task)

## Описание
  - [Test Task](https://github.com/ZOMini/deribit_api/blob/a721bdb39919a7ff8ce6e5f7efb6da92b21764f4/%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B5_%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5_junior_back_end_%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA.pdf) - тестировать проще через документацию.

## Стек
  - FastAPI, aiohttp, SQLAlchemy, Pytest, gunicorn, nginx, alembic, Postgres, apscheduler

## Запуск
  - Заполняем .env (см. .env.template в корне, можно просто сделать из него .env, он заполнен).
  - docker-compose up --build
  - Воркер в отдельном докере.
  - Миграции см. ниже.
  - Тесты автоматом в docker-compose(deribit_tests).

## Миграции
  - Инит миграции через алембик(алембик подкручен - зависит от .env).
  - Доп. миграции, если необходимо, то из папки deribit_api:
    - alembic revision -m "migration2" --autogenerate
    - alembic upgrade head

## URL
  - http://127.0.0.1/deribit/api/openapi - документация.

  


