# Generated by Django 4.1.5 on 2023-01-23 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0007_establishment_contact_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='address_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.address'),
            preserve_default=False,
        ),
    ]
