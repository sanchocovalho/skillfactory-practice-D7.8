# Задание D7.8

   Продолжение проекта домашней библиотеки. Функционал включает следующие моменты:

  - Через панель администратора: возможно добавление, изменение и удаление книг, авторов, друзей, издательств, обложек книг;
  - Без администратора возможно добавление и изменение книг, авторов, друзей, изданий, обложек книг.
  - Добавлен к проекту процесс авторизации на базе Django.

Для того, чтобы запустить локальный сервер необходимо:
1) Распакуйте проект в папку C:\my_site
2) Откройте командную строку и зайдите в директорию проекта:
   - cd C:\my_site
3) Создате виртуальное окружение:
   - python -m venv django
4) Активируйте виртуальное окружение:
   - django\Scripts\activate.bat
5) Установите все необходимые пакеты:
   - pip install -r requirements.txt
6) Запустите локальный сервер:
   - python manage.py runserver

Для того, чтобы сделать деплой на heroku необходимо:
1) Изменить в settings.py:
   - SECRET_KEY = 'Ваш_секретный_код' на SECRET_KEY = os.environ.get('SECRET_KEY')
   - ALLOWED_HOSTS = ['*']
   - DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': os.path.join(BASE_DIR, 'db.sqlite3'),}} на import dj_database_url и DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}
   - STATIC_URL = '/static/' на STATIC_URL = '/asset-v1:SkillFactory+PWS-1+5JUN2019+type@asset+block@/' и STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
2) Перейти в каталог с проектом:
   - cd C:\my_site
3) Выпонить следующий команды:
   - git init
   - git add .
   - git commit -m "initial commit
   - heroku login
   - heroku create
   - heroku addons:create heroku-postgresql --as DATABASE
   - heroku config:set SECRET_KEY=Ваш_секретный_код
   - git push heroku master
   - heroku run python manage.py loaddata data.xml
   - heroku run python manage.py createsuperuser
4) Если необходимо переименовываем приложение:
   - heroku rename -a oldname newname
5) Запускаем приложение:
   - heroku open
