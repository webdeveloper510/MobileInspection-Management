# Generated by Django 4.1.5 on 2023-01-21 05:51

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0004_rename_establishment_id_establishment_contact_establishment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment_contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=250, null=True, region=None),
        ),
    ]
