# Generated by Django 3.2.12 on 2023-01-16 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0012_alter_service_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_address',
            name='address_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.address'),
        ),
    ]
