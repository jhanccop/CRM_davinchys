# Generated by Django 5.0.6 on 2024-12-14 22:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0040_bankmovements_origindestination'),
        ('pedidos', '0012_alter_paymentrequest_pdf_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='idList',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Id Documento'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='currencyType',
            field=models.CharField(blank=True, choices=[('0', 'S/.'), ('1', '$'), ('2', '€')], max_length=1, null=True, verbose_name='Moneda'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='paymentType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movimientos.expensesubcategories'),
        ),
    ]
