# Generated by Django 3.2.12 on 2023-01-06 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='address1',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='comment',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='unit_number',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
