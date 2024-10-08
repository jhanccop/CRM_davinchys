# Generated by Django 5.0.6 on 2024-07-20 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0009_alter_trafoquote_deadline'),
        ('clientes', '0002_alter_cliente_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafoquote',
            name='idClient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='clientes.cliente'),
        ),
        migrations.AlterField(
            model_name='trafoquote',
            name='idQuote',
            field=models.CharField(max_length=100, unique=True, verbose_name='RFQ Number'),
        ),
    ]
