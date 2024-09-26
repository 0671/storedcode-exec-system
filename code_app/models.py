from django.db import models

# Create your models here.
class StoreCode(models.Model):
    code = models.TextField()
    last_task_id = models.CharField(max_length=100, default='',)
    created_at = models.DateTimeField(auto_now_add=True)