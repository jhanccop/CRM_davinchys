# Generated by Django 5.0.6 on 2024-12-19 10:54

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('full_name', models.CharField(max_length=100, verbose_name='Nombres')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phoneNumber', models.CharField(blank=True, null=True, verbose_name='Telefono')),
                ('area', models.CharField(blank=True, choices=[('0', 'Direccion'), ('1', 'Administracion'), ('2', 'Ventas'), ('3', 'Produccion'), ('4', 'Contabilidad'), ('5', 'Desarrollo')], max_length=1, verbose_name='Area en la Empresa')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Género')),
                ('condition', models.CharField(blank=True, choices=[('0', 'Activo'), ('1', 'Cesado'), ('2', 'Licencia'), ('3', 'Vacaciones')], max_length=1, verbose_name='Condicion')),
                ('currency', models.CharField(blank=True, choices=[('0', 'Soles'), ('1', 'Dolares')], max_length=1, verbose_name='Tipo de moneda de remuneracion')),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salario mensual')),
                ('date_entry', models.DateField(blank=True, null=True, verbose_name='Fecha de contratacion')),
                ('date_termination', models.DateField(blank=True, null=True, verbose_name='Fecha de cese')),
            ],
            options={
                'verbose_name': 'Colaborador',
                'verbose_name_plural': 'Colaboradores',
            },
        ),
    ]
