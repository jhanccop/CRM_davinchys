# Generated by Django 5.0.6 on 2024-07-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0011_remove_trafoquote_quotestatus_trafoquote_dt1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafoquote',
            name='q1',
            field=models.CharField(choices=[('4', 'creado'), ('0', 'espera'), ('1', 'completado'), ('3', 'observado'), ('2', 'cancelado')], default='1', max_length=1, verbose_name='Recibido'),
        ),
        migrations.AlterField(
            model_name='trafoquote',
            name='q2',
            field=models.CharField(choices=[('4', 'creado'), ('0', 'espera'), ('1', 'completado'), ('3', 'observado'), ('2', 'cancelado')], default='0', max_length=1, verbose_name='Cotizacion'),
        ),
        migrations.AlterField(
            model_name='trafoquote',
            name='q3',
            field=models.CharField(choices=[('4', 'creado'), ('0', 'espera'), ('1', 'completado'), ('3', 'observado'), ('2', 'cancelado')], default='0', max_length=1, verbose_name='Respuesta de cliente'),
        ),
        migrations.AlterField(
            model_name='trafoquote',
            name='q4',
            field=models.CharField(choices=[('4', 'creado'), ('0', 'espera'), ('1', 'completado'), ('3', 'observado'), ('2', 'cancelado')], default='0', max_length=1, verbose_name='Atendido'),
        ),
    ]
