# Generated by Django 5.0.6 on 2024-12-19 10:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actividades', '0002_initial'),
        ('clientes', '0001_initial'),
        ('movimientos', '0002_initial'),
        ('pedidos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='idPetitioner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitante', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='idProjects',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.projects'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='idProvider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='idTrafoOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.trafoorder'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='paymentType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EsubCategory', to='movimientos.expensesubcategories'),
        ),
        migrations.AddField(
            model_name='requestlist',
            name='idPetitioner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lista_solicitante', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='idList',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lista', to='pedidos.requestlist'),
        ),
    ]
