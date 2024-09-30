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

code example:
```python
from code_app.models import StoreCode
import time

class MyClass():
    def __init__(self):
        self.result = []
    def run(self):
        for i in StoreCode.objects.all():
            self.result.append(f'{i.id}:{int(time.time())}')
            time.sleep(5)
        return self.result
    def run_special(self,data):
        time.sleep(5)
        return f'{data}:{int(time.time())}'
```