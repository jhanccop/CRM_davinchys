# Generated by Django 5.0.6 on 2025-07-13 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0016_pettycash_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pettycashitems',
            options={'ordering': ['created'], 'verbose_name': 'Item de caja chica', 'verbose_name_plural': 'Items de caja chica'},
        ),
        migrations.RemoveField(
            model_name='pettycashitems',
            name='currency',
        ),
    ]
