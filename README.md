# storedcode-exec-system

## Need
1. python3.10
2. redis

## Prepare
```bash
pip install -r requirements.txt
```
modify redis config: myproject\myproject\settings.py -> CELERY_BROKER_URL


## Run
Run system
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 
```
Run celery
```bash
celery -A myproject worker -l info -P threads
```

## Access
http://127.0.0.1:8000/code/
