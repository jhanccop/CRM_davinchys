# Generated by Django 5.0.6 on 2024-08-29 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0019_alter_bankmovements_idmovement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankmovements',
            name='idMovement',
        ),
        migrations.AddField(
            model_name='bankmovements',
            name='idMovement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movimientos.bankmovements'),
        ),
    ]
