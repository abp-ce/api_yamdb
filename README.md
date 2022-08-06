# YAMDB API
База отзывов пользователей о фильмах, книгах и музыке.
#
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/abp-ce/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать директорию для email:

```
mkdir api_yamdb/sent_emails
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Стек
- Django 2.2.16
- djangorestframework 3.12.4
- djangorestframework-simplejwt 5.2.0