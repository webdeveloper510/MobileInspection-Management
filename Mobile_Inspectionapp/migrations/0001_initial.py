# Generated by Django 3.2.12 on 2022-12-17 07:05

import Mobile_Inspectionapp.validater
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_number', models.CharField(max_length=500)),
                ('unit_number', models.CharField(max_length=500)),
                ('addressline1', models.CharField(max_length=500)),
                ('addressline2', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('state', models.CharField(max_length=500)),
                ('postal_code', models.CharField(max_length=500)),
                ('country_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('squarefeet', models.CharField(max_length=250)),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.address')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=500)),
                ('lastname', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Operater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=500)),
                ('lastname', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=50)),
                ('operater_type', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=1000)),
                ('discount_rate', models.FloatField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=1000)),
                ('service_image', models.ImageField(blank=True, null=True, upload_to='products_images/')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_agreement_form', models.FileField(blank=True, null=True, upload_to='agreement_form/')),
                ('signature', models.FileField(blank=True, null=True, upload_to='signature/')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=255)),
                ('Last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, validators=[Mobile_Inspectionapp.validater.validate_mail])),
                ('title', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=255)),
                ('attribute_name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=50)),
                ('ifLogged', models.BooleanField(default=False)),
                ('token', models.CharField(default='', max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type_name', models.CharField(max_length=500)),
                ('price', models.FloatField()),
                ('service_agreement_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.serviceagreement')),
            ],
        ),
        migrations.AddField(
            model_name='serviceagreement',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.user'),
        ),
        migrations.CreateModel(
            name='Service_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(max_length=250)),
                ('service_datetime', models.DateTimeField()),
                ('service_fee', models.FloatField()),
                ('total_amount', models.FloatField()),
                ('requested_service_datetime', models.DateTimeField()),
                ('Establishment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.establishment')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.user')),
                ('operater_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.operater')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.service')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='service_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.servicetype'),
        ),
        migrations.CreateModel(
            name='Promotion_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.promotion')),
                ('service_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.servicetype')),
            ],
        ),
        migrations.CreateModel(
            name='LeadAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_number', models.CharField(max_length=500)),
                ('unit_number', models.CharField(max_length=500)),
                ('addressline1', models.CharField(max_length=500)),
                ('addressline2', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('state', models.CharField(max_length=500)),
                ('postal_code', models.CharField(max_length=500)),
                ('country_name', models.CharField(max_length=500)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.lead')),
            ],
        ),
        migrations.AddField(
            model_name='establishment',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.user'),
        ),
        migrations.AddField(
            model_name='address',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mobile_Inspectionapp.user'),
        ),
    ]
