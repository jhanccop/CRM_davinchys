# Generated by Django 5.0.6 on 2025-05-17 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0008_dailytasks_idrestday'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='restdays',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='restdays',
            name='dt1',
            field=models.DateTimeField(blank=True, null=True, verbose_name='F. RRHH'),
        ),
        migrations.AddField(
            model_name='restdays',
            name='dt2',
            field=models.DateTimeField(blank=True, null=True, verbose_name='F. Gerencia '),
        ),
        migrations.AddField(
            model_name='restdays',
            name='tag1',
            field=models.CharField(blank=True, choices=[('0', 'espera'), ('1', 'aceptado'), ('2', 'denegado'), ('3', 'observado'), ('4', 'creado')], default='0', max_length=1, null=True, verbose_name='Ap RRHH'),
        ),
        migrations.AddField(
            model_name='restdays',
            name='tag2',
            field=models.CharField(blank=True, choices=[('0', 'espera'), ('1', 'aceptado'), ('2', 'denegado'), ('3', 'observado'), ('4', 'creado')], default='4', max_length=1, null=True, verbose_name='VB Gerencia'),
        ),
    ]
