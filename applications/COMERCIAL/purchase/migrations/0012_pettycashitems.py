# Generated by Django 5.0.6 on 2025-07-12 11:47

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0011_remove_requirements_area_remove_requirements_idtin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PettyCashItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('quantity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad')),
                ('currency', models.CharField(blank=True, choices=[('0', 'PEN'), ('1', 'USD'), ('2', 'EUR')], max_length=1, null=True, verbose_name='Moneda')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Precio')),
                ('product', models.CharField(blank=True, max_length=150, null=True, verbose_name='Producto')),
                ('category', models.CharField(blank=True, choices=[('0', 'Transporte'), ('1', 'Envíos'), ('2', 'Alimentación'), ('3', 'Comunicaciones'), ('4', 'Otros')], max_length=1, null=True, verbose_name='Categoria')),
                ('idPettyCash', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requirementItems_requirement', to='purchase.pettycash')),
            ],
            options={
                'verbose_name': 'Item de requerimiento',
                'verbose_name_plural': 'Items de requerimientos',
                'ordering': ['created'],
            },
        ),
    ]
