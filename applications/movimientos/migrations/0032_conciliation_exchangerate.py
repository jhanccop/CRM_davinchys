# Generated by Django 5.0.6 on 2024-10-02 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0031_conciliation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='conciliation',
            name='exchangeRate',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=4, verbose_name='Tipo de cambio'),
        ),
    ]
