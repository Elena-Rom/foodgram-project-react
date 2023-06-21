# Проект Foodgram
![Github actions](https://github.com/Elena-Rom/foodgram-project-react/actions/workflows/main.yml/badge.svg)


### Описание
Проект "Foodgram" – это "продуктовый помощник". На этом сервисе авторизированные пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Для неавторизированных пользователей доступны просмотр рецептов и страниц авторов. 

## Стэк технологий:
- Python
- Django Rest Framework
- Postgres
- Docker

### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). 
- Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Как запустить проект на боевом сервере:

Установить на сервере docker и docker-compose.
Скопировать на сервер файлы docker-compose.yaml и default.conf:
```
scp docker-compose.yaml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yaml
scp default.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx/default.conf
```
Добавить в Secrets на Github следующие данные:
```
DB_ENGINE=django.db.backends.postgresql # указать, что проект работает с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
USER= # Логин на удалённом сервере
SSH_KEY= # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram
TELEGRAM_TOKEN= #ID бота в Telegram
```

Выполнить команды:
* git add .
* git commit -m "<commit>"
* git push

После этого будут запущены процессы workflow:
* проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
* сборка и доставка докер-образа для контейнера backend и frontend на Docker Hub
* автоматический деплой проекта на боевой сервер
* отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

После успешного завершения процессов workflow на боевом сервере необходимо выполнить следующие команды:
```
sudo docker-compose exec web python manage.py migrate
```
```
sudo docker-compose exec web python manage.py createsuperuser
```
```
sudo docker-compose exec backend python manage.py collectstatic --no-input 
```
  
### После каждого обновления репозитория (`git push`) будет происходить:
1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final
2. Сборка и доставка докер-образов на Docker Hub.
3. Автоматический деплой.
4. Отправка уведомления в Telegram.

### Как запустить проект локально для тестирования(бэк локально - фронт в контейнере):
1. Изменить nginx на:
upstream foodgram_backend{
    server host.docker.internal:8000;
}

server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri /index.html;
    }
    location /media/ {
        autoindex on;
         root /var/html/;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /var/html/frontend/;
    }

    location ~ ^/(api|admin)/(?!docs/) {
        proxy_set_header    Host $host;
        proxy_set_header    X-Real-IP $remote_addr;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Forwarded-Proto $scheme;
        proxy_pass http://foodgram_backend;
    }

    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/redoc.htmI;
    }
}
2. Добавить в docker-compose.yml строчку к контейнеру nginx:
extra_hosts:
  - 'host.docker.internal:host-gateway'
3. Собрать контейнеры - nginx и frontend:  docker-compose up -d 
4. Выполнить команды: 
 python manage.py createsuperuser (создать супер юзера)
 python3 manage.py runserver
5. Супер юзером перейти в <local host>/admin
6. Создать несколько тэгов

