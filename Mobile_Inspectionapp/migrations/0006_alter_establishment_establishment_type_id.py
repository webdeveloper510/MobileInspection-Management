# Generated by Django 4.1.5 on 2023-01-23 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0005_alter_establishment_contact_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='establishment_type_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.establishment_type'),
        ),
    ]
