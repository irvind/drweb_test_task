Тестовое задание
================

Описание
--------

Приложение состоит из двух компонентов:

- Django-приложение
- Воркер

Приложение и воркер нужно запускать одновременно.


Зависимости
-----------

* Python 3
* PostgresSQL
* База данных и пользователь с правами для этой бд


Установка
---------

    virtualenv drweb_test_task_env
    . drweb_test_task_env/bin/activate

    git clone git@github.com:irvind/drweb_test_task.git
    cd drweb_test_task
    pip install -r requirements.txt

    cd project
    cp project/local_settings.py.tmpl project/local_settings.py

    # Указать данные авторизации для БД
    vim project/local_settings.py

    ./manage.py migrate
    ./manage.py runserver

    # Можно запустить во втором терминале
    python worker.py
