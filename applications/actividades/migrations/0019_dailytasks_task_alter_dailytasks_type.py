# Generated by Django 5.0.6 on 2025-05-23 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0018_remove_dailytasks_endtime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailytasks',
            name='task',
            field=models.CharField(blank=True, choices=[('0', 'Inspección'), ('1', 'Mantenimiento'), ('2', 'Producción'), ('3', 'Control de calidad'), ('4', 'Transporte'), ('5', 'Logistica'), ('6', 'Documentación'), ('7', 'Reunión'), ('8', 'Marketing'), ('9', 'Planificación'), ('10', 'Finanzas'), ('11', 'Contabilidad'), ('12', 'Representación'), ('13', 'Auditoria'), ('14', 'Desarrollo'), ('15', 'Testing'), ('16', 'Aduanas'), ('17', 'Otro')], default='7', max_length=2, null=True, verbose_name='Tipo de actividad'),
        ),
        migrations.AlterField(
            model_name='dailytasks',
            name='type',
            field=models.CharField(blank=True, choices=[('0', 'Jornada diaria'), ('1', 'Horas extra'), ('2', 'Feriado'), ('4', 'Compensación'), ('3', 'Otro')], default='0', max_length=1, null=True, verbose_name='Tipo de jornada'),
        ),
    ]
