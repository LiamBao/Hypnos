# Generated by Django 2.0.1 on 2018-01-30 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celery_test', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='move_at',
        ),
    ]
