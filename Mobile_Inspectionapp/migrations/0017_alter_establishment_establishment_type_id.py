# Generated by Django 4.1.5 on 2023-01-24 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0016_alter_establishment_establishment_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='establishment_type_id',
            field=models.ForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.establishment_type'),
        ),
    ]
