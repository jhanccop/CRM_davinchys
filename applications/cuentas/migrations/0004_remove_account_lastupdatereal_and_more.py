# Generated by Django 5.0.6 on 2024-08-15 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0003_tin_account_idtin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='lastUpdateReal',
        ),
        migrations.RemoveField(
            model_name='account',
            name='realBalance',
        ),
    ]