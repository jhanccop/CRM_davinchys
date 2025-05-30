# Generated by Django 5.0.6 on 2025-05-26 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0010_remove_cliente_electronicsignature_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='electronicSignature',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Firma electrónica'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='internationalBilling',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Facturación internacional'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='legalJurisdiction',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Jurisdicción legal aplicable'),
        ),
    ]
