# test_restaurants
Реализован функционал:  
- собирает информацию о ресторанах "McDonalds", "Burger King", "KFC"
- выводит список ресторанов "Burger King" с указанием для каждого ресторана количества ресторанов конкурентов, находящихся на расстоянии менее 2-х км.

## Как развернуть приложение
Склонировать репозиторий.  
Перейти в каталог с проектом: test_restaurant/  
Создать и активировать виртуальное окружение, установить зависимости:
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
Выполнить миграции:  
```
cd restaurants
python manage.py makemigrations
python manage.py migrate
```
Создать список компаний (создаются компании "McDonalds", "Burger King", "KFC". В случае необходимости добавлять/удалять компании можно через интерфейс администратора):
```
python manage.py company
```
При необходимости создать суперпользователя:
```
python manage.py createsuperuser
```
Запустить сервер отладки:
```
python manage.py runserver
```
  
## Использование приложения
Получение информации о ресторанах и внесение её в базу данных (POST-запрос):
```
 http://127.0.0.1:8000/restaurants/update/
```
Получение списка ресторанов "Burger King" (GET-запрос):
```
http://127.0.0.1:8000/restaurants/burger_king/
```
Интерфейс администратора:
```
http://127.0.0.1:8000/admin/
```