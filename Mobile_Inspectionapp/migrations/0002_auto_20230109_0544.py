# Generated by Django 3.2.12 on 2023-01-09 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
    ]
