# Generated by Django 5.0.6 on 2024-08-30 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0021_bankmovements_conciliated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankmovements',
            name='idMovement',
        ),
        migrations.AddField(
            model_name='bankmovements',
            name='idMovement',
            field=models.ManyToManyField(blank=True, to='movimientos.bankmovements'),
        ),
    ]