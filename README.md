
<h1 align="center">Сервис баннеров</h1>

## Стек

Cервис: Python, Django, DRF, Celery, Celery-beat, Redis, Flake8

База данных: PostgreSQL

Для деплоя зависимостей и самого сервиса использовал Docker и Docker Compose.

## Инструкция по запуску:

1. Клонирование репозитория на примере VS Code:
   
- выбираем "Clone Git Repository..."
- вставляем адрес
     
```shell
https://github.com/electr0n4ik/banner_service.git
```
2. Запуск через docker-compose:
   
- открываем новый терминал
- останавливаем редис, если он запущен
 
```shell
sudo systemctl stop redis
```

- запускаем команду для сборки
 
```shell
docker-compose -f docker-compose.local.yaml --env-file .env up --build
```

- видим запущенный сервер по адресу http://0.0.0.0:8888/
  
![image](https://github.com/electr0n4ik/banner_service/assets/116460003/6636dbb3-d0d0-4675-bdda-7be79c345c91)

- (**ОПЦИОНАЛЬНО**) далее открываем второй терминал и запускаем кастомную команду для автоматического наполнения БД.
  
```shell
docker exec -ti banner_service_app python manage.py put_data --n_features=1000 --clear
```
- флаг "--clear" **опциональный**, удаляет данные в двух таблицах с обнулением первичных ключей. С помощью этой команды можно регулировать количество записей в БД, во флаге "--n_features=<количество фич>" передаем количество фич для создания записей. Количество созданный записей будет выведено в командную строку.

## Описанные вопросы/проблемы

#### 1. Для однозначного поиска, было принято решение, запретить создание записи в БД по следующей логике:

С одной фичей не могут быть одни и те же теги, но одни и те же теги могут быть у разных баннеров, так же и с фичами, одни и те же фичи могут быть у нескольких баннеров одновременно.

#### 2. В АПИ используются токены. Добавил отдельный урл для получения токенов. Токен существует 1 час.

Пример запроса curl в конце README-файла.

**Для передачи токена использовать header - Authorization. Токен передавать без Bearer**

Описание работы отдельного урла:

```shell
http://0.0.0.0:8888/token/
```

По данному пути необходимо выполнять POST-запросы с телом запроса:

```shell
{
    "is_admin": true,
    "username": "user_admin_1",
    "password": "12345678"
}
```

```shell
{
    "is_admin": false,
    "username": "user_1",
    "password": "12345678"
}
```

Ключ "is_admin" работает только при создании пользователя. Запрос с данными существующего пользователя вернет токен.
Пример ответа для нового админа:

```shell
{
    "detail": "admin_created",
    "admin_token": "69c8d7fca3fbfe83"
}
```
Пример ответа для существующего админа:

```shell
{
    "detail": "Account was found",
    "admin_token": "69c8d7fca3fbfe83"
}
```

Пример ответа для нового юзера:

```shell
{
    "detail": "user_created",
    "user_token": "7a0298f4ff0824b3fb6cbb846d814da6"
}
```

Пример ответа для существующего юзера:

```shell
{
    "detail": "Account was found",
    "user_token": "45e79ed46099344ce1f8187711c65fbf"
}
```

#### 3. Адаптировал систему для значительного увеличения количества тегов и фичей. Создал кастомную команду, с помощью которой можно автоматически наполнить БД.
#### 4. Изменил API таким образом, чтобы можно было просмотреть существующие версии баннера и выбрать подходящую версию. Добавил метод GET в урл:

```shell
http://0.0.0.0:8888/banner/<int:id>/
```

После запроса с **админским токеном** вернутся версии баннера. Поясняю, первая версия баннера нулевая, каждый созданный баннер получает нулевую версию. Все версии сохраняются для дальнейшей возможности откатиться на них.

Пример баннера без изменений:
```shell
{
    "current_version": {
        "feature_id": 3055,
        "tag_ids": [
            7
        ],
        "title": "title",
        "description": "description",
        "url": "https://www.avito.ru/я-вас-люблю",
        "is_active": true,
        "current_version": 0
    },
    "last_versions": []
}
```

Пример баннера с несколькими версиями:
```shell
{
    "current_version": {
        "feature_id": 2222,
        "tag_ids": [
            22222
        ],
        "title": "2222",
        "description": "2222",
        "url": "2222",
        "is_active": true,
        "current_version": 2
    },
    "last_versions": [
        {
            "url": "1111",
            "title": "1111",
            "tag_ids": [
                11111
            ],
            "is_active": true,
            "feature_id": 11111,
            "description": "1111",
            "current_version": 0
        },
        {
            "url": "2222",
            "title": "2222",
            "tag_ids": [
                22222
            ],
            "is_active": true,
            "feature_id": 2222,
            "description": "2222",
            "current_version": 1
        }
    ]
}
```

Для отката текущих данных баннера на определенную версию необходимо выполнить PATCH-запрос по пути:

```shell
http://0.0.0.0:8888/banner/<int:id>/
```

В теле запроса необходимо передать ключ "banner_version":

```shell
{
    "banner_version": 0
}
```

В ответ получаем:

```shell
{
    "OK": "Баннер №6 найден и изменен с версии 2 на 1"
}
```

Как итог повторный GET-запрос выдает такие данные:

```shell
{
    "current_version": {
        "feature_id": 11111,
        "tag_ids": [
            11111
        ],
        "title": "1111",
        "description": "1111",
        "url": "1111",
        "is_active": true,
        "current_version": 0
    },
    "last_versions": [
        {
            "url": "1111",
            "title": "1111",
            "tag_ids": [
                11111
            ],
            "is_active": true,
            "feature_id": 11111,
            "description": "1111",
            "current_version": 0
        },
        {
            "url": "2222",
            "title": "2222",
            "tag_ids": [
                22222
            ],
            "is_active": true,
            "feature_id": 2222,
            "description": "2222",
            "current_version": 1
        }
    ]
}
```

Следует заметить наличие всех сохраненных версий, успешное изменение версии без создания новой версии.

#### 5. Добавил метод удаления баннеров по фиче или тегу, время ответа которого не превышает 100 мс, независимо от количества баннеров. Использовал механизм выполнения отложенных задач. Для этого изменил АПИ таким образом, чтобы по пути banner/ можно было использовать метод DELETE.

Пример запроса curl:

```shell
curl --location --request DELETE 'http://0.0.0.0:8888/banner/' \
--header 'Authorization: f0b86b57dfb71f08' \
--header 'Content-Type: application/json' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah' \
--data '{
    "tag_ids": [
        700
    ],
    "feature_id": 1
}'
```
Метод поддерживает одновременный прием tag_ids и feature_id.

#### 6. Описал конфигурацию линтера.

Запуск

```shell
docker exec -ti banner_service_app flake8
```

Успешная проверка не выдает ошибок.

## CURLs

**user_banner/**

**GET**

```shell
curl --location 'http://0.0.0.0:8888/user_banner/?feature_id=1&use_last_revision=true&tag_id=1' \
--header 'Authorization: 38de5aa5bbd1c324' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah'
```

**banners/**

**GET**

```shell
curl --location --request GET 'http://0.0.0.0:8888/banner/?offset=0&limit=1000' \
--header 'Authorization: 38de5aa5bbd1c324' \
--header 'Content-Type: application/json' \
--header 'Cookie: sessionid=uye0ah96j266iyakv1j6qsh40dht5osi' \
--data '{}'
```

**POST**

```shell
curl --location 'http://0.0.0.0:8888/banner/' \
--header 'Authorization: f0b86b57dfb71f08' \
--header 'Content-Type: application/json' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah' \
--data '{
    "tag_ids": [
        700
    ],
    "feature_id": 1,
    "content": {
        "title": "1new_title", 
        "text": "2new_text", 
        "url": "3new_url"
    },
    "is_active": true
}'
```

**DELETE**

```shell
curl --location --request DELETE 'http://0.0.0.0:8888/banner/' \
--header 'Authorization: f0b86b57dfb71f08' \
--header 'Content-Type: application/json' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah' \
--data '{
    "tag_ids": [
        700
    ],
    "feature_id": 1
}'
```

**banner/<int:id>/**

**GET**

```shell
curl --location 'http://0.0.0.0:8888/banner/1/' \
--header 'Authorization: f0b86b57dfb71f08' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah'
```

**POST**

```shell
curl --location 'http://0.0.0.0:8888/banner/1/' \
--header 'Authorization: f0b86b57dfb71f08' \
--header 'Content-Type: application/json' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah' \
--data '{
    "banner_version": 0,
    "tag_ids": [22222],
    "feature_id": 2222,
    "content": {
        "title": "2222", 
        "text": "2222", 
        "url": "2222"
    },
    "is_active": false
}'
```

**DELETE**

```shell
curl --location --request DELETE 'http://0.0.0.0:8888/banner/1/' \
--header 'Authorization: f0b86b57dfb71f08' \
--header 'Content-Type: application/json' \
--header 'Cookie: sessionid=5owraro2ameuk8mbuv3kzzrqqhoe55ah' \
--data '{
    "banner_version": 0
}'
```

**token/**

**POST**

```shell
curl --location 'http://127.0.0.1:8000/token/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=PTde1XAJjb3oF0x2ECYjFvrlY1XiMb0X; sessionid=yqqbc82lgpof1s3wwlualrdo2d09rfj2' \
--data '{
    "is_admin": true,
    "username": "user_admin_1",
    "password": "12345678"
}'
```
