# Generated by Django 5.1.1 on 2024-09-26 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storecode',
            name='last_task_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
