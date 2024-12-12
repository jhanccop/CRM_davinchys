# Generated by Django 5.0.6 on 2024-12-12 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_alter_cliente_bankname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='bankName',
            field=models.CharField(blank=True, choices=[('0', 'BCP'), ('1', 'BBVA'), ('2', 'INTERBANK'), ('3', 'SCOTIABANK'), ('4', 'COMERCIO'), ('5', 'BANBIF'), ('6', 'PICHINCHA'), ('7', 'GNB'), ('8', 'MIBANCO'), ('9', 'FALABELLA'), ('10', 'CITIBANK'), ('11', 'RIPLEY')], max_length=2, null=True, verbose_name='Banco'),
        ),
    ]
