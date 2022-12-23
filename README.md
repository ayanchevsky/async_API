# Домашнее задание по теме "Асинхронность"
## Отчет по продажам
Вы разрабатываете онлайн веб-приложение для генерации отчетов от сети продаж. Владельцы торговой сети (конечные пользователи системы) хотят оперативно получать отчеты о том как идут дела на их точках продаж, какая выручка, какие товары проданы и т.д. Системы внутри торговых точек (тоже конечные пользователи системы) должны используя ваш сервис отчитываться о совершенных продажах товаров чтобы централизованно происходил сбор таких данных. Продажи совершаются часто по этому имеет смысл заложить в сервис способность справляться с большими нагрузками.

## Требования

  - реализуйте асинхронное веб приложение которое
    - обрабатывает GET-запрос на получение всех товарных позиций
    - обрабатывает GET-запрос на получение всех магазинов
    - обрабатывает POST-запрос с json-телом для сохранения данных о произведенной продаже (id товара + id магазина)
    - обрабатывает GET-запрос на получение данных по топ 10 самых доходных магазинов за месяц (id + адрес + суммарная выручка)
    - обрабатывает GET-запрос на получение данных по топ 10 самых продаваемых товаров (id + наименование + количество проданных товаров)
    - никакие лишние эндпоинты реализовывать не требуется
  - напишите readme.md с кратким описанием эндпоинтов и инструкцией запуска
  - используйте requirements.txt для указания сторонних зависимостей и их версий
  - используйте postgres или sqlite в качестве базы.
  - используйте асинхронный веб-фреймворк на ваш выбор и асинхронный драйвер подключения к бд на ваш выбор.
  - в качестве ориентира модели данных можно(а можно и не) использовать приведенную ниже dbml схему (визуализировать ее можно инструментом dbdiagram.io). однако это не     обязательно, можно разработать собственное целевое понимание модели данных.
  
  ## Решение
  - реализовано асинхронное веб приложение которое:
    - обрабатывает GET-запрос на получение всех товарных позиций /items/
    - обрабатывает GET-запрос на получение всех магазинов /stores/
    - обрабатывает GET-запрос на получение всех продаж /sales/
    - обрабатывает POST-запрос с json-телом для сохранения данных о произведенной продаже (id товара + id магазина) /sales/
    - обрабатывает GET-запрос на получение данных по топ 10 самых доходных магазинов за месяц (id + адрес + суммарная выручка) /items/top/
    - обрабатывает GET-запрос на получение данных по топ 10 самых продаваемых товаров (id + наименование + количество проданных товаров) /stores/top/
  ## Дополнительно
  Зависимости в файле **requirements.txt**, примеры HTTP запросов в файле **requests.http**.

  База данных используется PostgreSQL со следующими настройками:
  ```
    DB_USER = "postgres"
    DB_NAME = "shop"
    DB_PASSWORD = "admin"
    DB_HOST = "127.0.0.1"
  ```
  и при каждом запуске выполняется удаление всех таблиц в БД и их пересоздание заполнение таблиц начальными данными запуском файла **add_date_to_db**.

    ```
    @app.on_event("startup")
    async def startup():
        # Drop and crate all tables in db 
        await init_models()
        # add new data to db
        add_date_to_db.add_date()
        print("Done")
    ``` 
  После создания таблиц и наполнения их данными эти строки можно закоментировать, для сохранения данных.

  Добавлен **валидатор** для проверки данных переданных в POST запросе и возврат требуемового кода ошибки **400**.
  
  Запуск осуществляется как стандартный скрипт или через команду: **uvicorn main:app --reload**
