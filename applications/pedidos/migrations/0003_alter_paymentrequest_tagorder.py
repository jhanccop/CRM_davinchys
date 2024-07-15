# Generated by Django 5.0.6 on 2024-07-10 20:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='tagOrder',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('0', 'solicitado'), ('1', 'aceptado'), ('2', 'denegado')], default='0', max_length=1, null=True, verbose_name='Estado'), blank=True, default=list, null=True, size=None),
        ),
    ]
