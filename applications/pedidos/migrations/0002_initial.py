# Generated by Django 5.0.6 on 2024-07-10 13:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actividades', '0002_initial'),
        ('clientes', '0001_initial'),
        ('pedidos', '0001_initial'),
        ('personal', '0001_initial'),
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
            name='idSupervisor',
            field=models.ManyToManyField(related_name='autorizantes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='idTrafoOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.trafoorder'),
        ),
        migrations.AddField(
            model_name='purchaseorders',
            name='idCommissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.commissions'),
        ),
        migrations.AddField(
            model_name='purchaseorders',
            name='idOrders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.orders'),
        ),
        migrations.AddField(
            model_name='purchaseorders',
            name='idProjects',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.projects'),
        ),
        migrations.AddField(
            model_name='purchaseorders',
            name='idWorker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personal.workers'),
        ),
        migrations.AddField(
            model_name='serviceorders',
            name='idClient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
        migrations.AddField(
            model_name='serviceorders',
            name='idCommissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.commissions'),
        ),
        migrations.AddField(
            model_name='serviceorders',
            name='idOrders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.orders'),
        ),
        migrations.AddField(
            model_name='serviceorders',
            name='idProjects',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.projects'),
        ),
        migrations.AddField(
            model_name='serviceorders',
            name='idWorker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personal.workers'),
        ),
    ]
