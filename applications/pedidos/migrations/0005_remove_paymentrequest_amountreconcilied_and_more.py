# Generated by Django 5.0.6 on 2024-07-12 00:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_alter_paymentrequest_tagorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrequest',
            name='amountReconcilied',
        ),
        migrations.RemoveField(
            model_name='paymentrequest',
            name='idSupervisor',
        ),
        migrations.RemoveField(
            model_name='paymentrequest',
            name='numbers',
        ),
        migrations.RemoveField(
            model_name='paymentrequest',
            name='tagOrder',
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='dt0',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='F. solicitada'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='dt1',
            field=models.DateTimeField(blank=True, null=True, verbose_name='F. adquisiciones'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='dt2',
            field=models.DateTimeField(blank=True, null=True, verbose_name='F. contabilidad '),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='dt3',
            field=models.DateTimeField(blank=True, null=True, verbose_name='F. finanzas'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='dt4',
            field=models.DateTimeField(blank=True, null=True, verbose_name='F. desembolso'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='observations',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Observaciones'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad'),
        ),
    ]
