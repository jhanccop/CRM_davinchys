# Generated by Django 5.0.6 on 2024-08-13 13:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0017_emailsent'),
        ('clientes', '0002_alter_cliente_email'),
        ('movimientos', '0005_alter_bankreconciliation_expensescategory_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BankReconciliation',
            new_name='Documents',
        ),
    ]
