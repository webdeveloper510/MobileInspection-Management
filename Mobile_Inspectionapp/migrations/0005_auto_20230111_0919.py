# Generated by Django 3.2.12 on 2023-01-11 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mobile_Inspectionapp', '0004_remove_address_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment_type',
            name='title',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Customer_Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.address')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.user')),
            ],
        ),
    ]
