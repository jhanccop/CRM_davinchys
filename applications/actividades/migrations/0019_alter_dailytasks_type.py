# Generated by Django 5.0.6 on 2024-08-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0018_alter_dailytasks_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytasks',
            name='type',
            field=models.BooleanField(default=False, verbose_name='Horas extra'),
        ),
    ]