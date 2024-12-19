# Generated by Django 5.0.6 on 2024-12-19 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0033_expensesubcategories_incomesubcategories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensesubcategories',
            name='category',
            field=models.CharField(blank=True, choices=[('0', 'Producto'), ('1', 'Compras activos'), ('2', 'Fijos'), ('3', 'Variables'), ('4', 'Impuestos'), ('5', 'Cambio de moneda'), ('6', 'Deducciones'), ('7', 'Retiros'), ('8', 'Otros')], default='8', max_length=1, null=True, verbose_name='Categoria'),
        ),
    ]
