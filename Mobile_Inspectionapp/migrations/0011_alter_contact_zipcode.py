# Generated by Django 3.2.12 on 2023-01-04 06:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0010_alter_contact_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='zipcode',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(6)]),
        ),
    ]
