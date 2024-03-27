# random_coffee_bot

## Описание проекта

Телеграм-Бот ЗАО "Groupe SEB". С помощью бота выбирается оффлайн и онлайн встречи 1-1 для сотрудников компании. Каждую неделю в случайном порядке подбирается пара для кофе-брейка. В конце недели приходит напоминание о встрече. Встречи проходят за пределами бота - на онлайн звонках, либо на личных встречах.

Функционал телеграм-бота:

- для пользователя: регистрация, получение пары, возможность на время отписаться от рассылки и не учавствовать в распределении пары
- для администратора: просмотр списка всех польхователей, возможность удалить пользователя, можно добавить пользователя в администраторы, а так же удалить его от туда, возможность отключения пользователя от рассылки

## Технологии

- **APScheduler**
- **aiogram**
- **SQLAlchemy**
- **alembic**
- **aiosqlite**
- **pydantic**

- [APScheduler](https://github.com/agronholm/apscheduler)
- [aiogram](https://github.com/aiogram/aiogram)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [aiosqlite](https://github.com/CXwudi/aiosqlite)
- [pydantic](https://pydantic-docs.helpmanual.io/)

## Запуск проекта в dev-режиме

- Примечание: для работы над проектом необходим Python не ниже версии 3.11.

1. Клонировать репозиторий и перейти в него в командной строке:

    ```bash
        git clone git@github.com:Studio-Yandex-Practicum/random_coffee_bot_anna.git
    ```

2. Создать виртуальное окружение:

    ```bash
        py -3.11 -m venv venv
    ```

3. Активировать виртуальное окружение:

    ```bash
        Windows: source venv/Scripts/activate
        Linux/macOS: source venv/bin/activate
    ```

4. Установить зависимости из файла requirements.txt:

    ```bash
        pip install -r requirements.txt
    ```

5. Создать файл .env и поместить в него:

    ```python
        # токен телеграм бота, формат string
        BOT_TOKEN=''
        DATABASE_URL='sqlite+aiosqlite:///./random_coffe_bot.db'
        # телеграм_id фдмина бота, формат string
        # если админов несколько добавить id последовательно, через пробел
        GEN_ADMIN_ID=''
    ```

6. Создать БД:

    ```bash
        alembic upgrade head
    ```

7. Запустить бота из главной директории:

    ```bash
        python bot.py
    ```

## Команда разработки

[Анна Победоносцева](https://github.com/ZebraHr) (тимлид команды)
[Светлана Шатунова](https://github.com/SvShatunova) (разработчик)
[Ольга Скрябина](https://github.com/ibonish) (разработчик)
[Татьяна Мусатова](https://github.com/Tatiana314) (разработчик)
[Никита Пискунов](https://github.com/Nikitkosss) (разработчик)
