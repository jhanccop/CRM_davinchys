# Generated by Django 5.0.6 on 2024-07-12 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0008_alter_paymentrequest_typerequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='observations',
            field=models.CharField(blank=True, default='Ninguna', max_length=100, null=True, verbose_name='Observaciones'),
        ),
    ]
