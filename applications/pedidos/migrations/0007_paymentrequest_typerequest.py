# Generated by Django 5.0.6 on 2024-07-12 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_paymentrequest_tag1_paymentrequest_tag2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='typeRequest',
            field=models.CharField(blank=True, choices=[('0', 'simple'), ('1', 'contabilidad')], max_length=2, null=True, verbose_name='Moneda'),
        ),
    ]
