# Generated by Django 3.2.12 on 2022-11-14 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=500)),
            ],
        ),
    ]
