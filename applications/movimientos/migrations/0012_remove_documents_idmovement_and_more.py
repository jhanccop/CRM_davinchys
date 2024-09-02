# Generated by Django 5.0.6 on 2024-08-27 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0011_documents_idmovement_documents_typeconciliation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='idMovement',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='typeConciliation',
        ),
        migrations.AddField(
            model_name='bankmovements',
            name='idMovement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movimientos.bankmovements'),
        ),
        migrations.AddField(
            model_name='bankmovements',
            name='typeConciliation',
            field=models.CharField(blank=True, choices=[('0', 'Documentaria'), ('1', 'Cambio de moneda'), ('2', 'Prestamo')], default='0', max_length=1, null=True, verbose_name='Tipo de conciliacion'),
        ),
    ]