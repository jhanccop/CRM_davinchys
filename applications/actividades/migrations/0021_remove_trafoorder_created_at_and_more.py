# Generated by Django 5.0.6 on 2024-09-16 11:51

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0020_rename_type_dailytasks_is_overtime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trafoorder',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='trafoorder',
            name='updated_at',
        ),
        migrations.CreateModel(
            name='TrafoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('nameTask', models.CharField(max_length=100, verbose_name='Tarea')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ubicacion')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Fecha de inicio')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Fecha finalizacion')),
                ('progress', models.IntegerField(default=0, verbose_name='Progreso')),
                ('is_milestone', models.BooleanField(default=False)),
                ('depend', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='actividades.trafotask')),
                ('trafoQuote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.trafoorder')),
            ],
            options={
                'verbose_name': 'Tarea orden',
                'verbose_name_plural': 'Tareas ordenes',
            },
        ),
    ]
