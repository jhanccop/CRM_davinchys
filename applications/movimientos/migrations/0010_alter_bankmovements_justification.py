# Generated by Django 5.0.6 on 2025-04-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0009_alter_bankmovements_justification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankmovements',
            name='justification',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Justification'),
        ),
    ]
