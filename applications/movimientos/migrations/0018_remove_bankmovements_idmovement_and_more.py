# Generated by Django 5.0.6 on 2024-08-28 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0017_remove_bankmovements_idmovement_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankmovements',
            name='idMovement',
        ),
        migrations.AddField(
            model_name='bankmovements',
            name='idMovement',
            field=models.ManyToManyField(blank=True, related_name='movs', to='movimientos.bankmovements'),
        ),
    ]
