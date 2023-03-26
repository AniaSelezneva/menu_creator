# Menu Creator

Приложение реализовывает древовидное меню, основываясь на данных, полученных из БД.

Данные добавляются через стандартную админку.

Активный пункт меню определяется исходя из URL текущей страницы.

## Установка и запуск

* Клонируйте репозиторий проекта с GitHub: `git clone https://github.com/AniaSelezneva/menu_creator.git`
* Примените миграции: `python3 manage.py migrate`
* Создайте нового суперпользователя для админки: `python3 manage.py createsuperuser`
* Запустите сервер: `python3 manage.py runserver`


- По умолчанию приложение доступно локально по адресу: http://localhost:8000/
- Админка: http://localhost:8000/admin