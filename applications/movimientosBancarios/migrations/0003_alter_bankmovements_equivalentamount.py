# Generated by Django 5.0.6 on 2025-05-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientosBancarios', '0002_alter_bankmovements_origindestination_bankvoucher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankmovements',
            name='equivalentAmount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Monto equivalente'),
        ),
    ]
