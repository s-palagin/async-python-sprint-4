## Сервис коротких ссылок

Для запуска сервиса склонируйте репозиторй и перейдите в папку с проектом.
Установите и активируйте виртуальное окружение:
```
$ python -m venv venv
$ . venv/bin/activate
```
Установите зависимости из файла requirrements.txt:
```
$ pip install -r requirements.txt
```
Перейдите в папку ```src``` и создайте файл `.env`. Укажите в нем настройки доступа к базе данных PostgreSQL в следующем формате - `DATABASE_DSN=driver://user:pass@localhost/dbname`. Для тестирования возможно запустить отдельный контейнер с PostgreSQL. Для этого выполните следующую команду:
```
sudo docker run --rm \
--name postgres-fastapi \
-p 5432:5432 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=collection \
-d postgres:14.5
```
Тогда в `.env` запишите следующую строку:

```
DATABASE_DSN=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
```
Так же в файле `.env` есть возможность указать имя для сервиса, адрес хоста и порт:
```
APP_TITLE="ShortLinkService"
PROJECT_PORT=8080
PROJECT_HOST='127.0.0.1'
```

Перед первым запуском проекта необходимо подготовить БД - выполнить миграции.
Для этого выполните команду:
```
$ alembic upgrade head
```

Запустить сервис можно командой:
```
$ python main.py
```

Документация доступна после запуска сервиса по адресу `http://127.0.0.1:8080/api/openapi`

В проекте реализован **middlware**, блокирующий доступ к сервису запросов из запрещенных подсетей (black list).
Список запрещенных подсетей находится в файле `src/utils/settings.py`



# Проектное задание четвертого спринта

Спроектируйте и реализуйте сервис для создания сокращенной формы передаваемых URL и анализа активности их использования.

Кроме этого, выберите из списка дополнительные требования и тоже реализуйте их. У каждого задания есть определённая сложность, от которой зависит количество баллов. Вам необходимо выбрать такое количество заданий, чтобы общая сумма баллов была больше 4. Выбор заданий никак не ограничен: можно выбрать все простые или одно среднее и два простых, или одно продвинутое, или решить все.

## Описание задания

Реализовать **http**-сервис, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080`.


<details>
<summary> Список необходимых эндпойнтов (можно изменять) </summary>

1. Получить сокращенный вариант переданного URL
```python
POST /
```

Request
```json
https://...
```

Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`.


2. Вернуть оригинальный URL
```python
GET /<url_id>
```
Метод принимает в качестве параметра идентификатор сокращенного URL и возвращает ответ с кодом `307` и оригинальным URL в заголовке `Location`.

3. Вернуть статус использования URL
```python
GET /<url_id>/status?[full-info]&&[max-result=10]&&[offset=0]
```
Метод принимает в качестве параметра идентификатор сокращенного URL и возвращает информацию о количестве переходов, совершенных по ссылке.

В ответе может содержаться как общее количество совершенных переходов, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
- время перехода/использования ссылки;
- информация о клиенте, выполнившем запрос;

</details>



### Дополнительные требования (отметить [Х] выбранные пункты):

- [ ] (1 балл) Реализуйте метод `GET /ping`, который возвращает информацию о статусе доступности БД.
- [x] (1 балл) Реализуйте возможность "удаления" сохраненного URL. Запись должна оставаться, но помечаться как удаленная. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.

- [x] (2 балла) Реализуйте **middlware**, блокирующий доступ к сервису запросов из запрещенных подсетей (black list).
- [x] (2 балла) Реализуйте возможность передавать ссылки пачками (batch upload).

<details>
<summary> Описание изменений </summary>

- Метод `POST /shorten` принимает в теле запроса список URL в формате:
```python
[
    {
        "original_url": "URL for shorten"
    },
    ...
]

```
и возвращает данные в формате:
```python
[
    {
        "url_id": "<text-id>",
        "short_url": "https://...",
    },
    ...
]
```
</details>



- [ ] (3 балла) Реализуйте взаимодействие с сервисом авторизованного пользователя. Пользователь может создавать как приватные, так и публичные ссылки или изменять видимость ссылок. Вызов метода `GET /user/status` возвращает все созданные ранее ссылки в формате:

```
[
    {
        "short_id": "<text-id>",
        "short_url": "https://...",
        "original_url": "https://...",
        "type": "<public|private>"
    },
    ...
]
```

- [ ] **(5 баллов) Реализовать кастомную реализацию взаимодействия с БД. Учесть возможность работы с транзакциями.


## Требования к решению

1. Используйте фреймворк FastAPI. В качестве СУБД используйте PostgreSQL (не ниже 10).
2. Используйте концепции ООП.
3. Предусмотрите обработку исключительных ситуаций. 
4. Приведите стиль кода в соответствие pep8, flake8, mypy. 
5. Логируйте результаты действий. 
6. Покройте написанный код тестами. 
