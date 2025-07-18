# Generated by Django 5.0.6 on 2025-06-16 16:04

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0011_cliente_electronicsignature_and_more'),
        ('cuentas', '0003_alter_account_currency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrafoQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('idQuote', models.CharField(max_length=100, unique=True, verbose_name='RFQ Number')),
                ('dateOrder', models.DateField(verbose_name='Fecha de pedido')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Fecha de entrega')),
                ('poStatus', models.CharField(blank=True, choices=[('0', 'no PO'), ('1', 'PO')], default='0', max_length=1, null=True, verbose_name='Estado PO')),
                ('currency', models.CharField(blank=True, choices=[('0', 'USD'), ('1', 'PEN'), ('2', 'EUR')], default='0', max_length=1, null=True, verbose_name='Currency')),
                ('payMethod', models.CharField(blank=True, choices=[('0', 'Anticipo'), ('1', 'Total'), ('2', 'Final'), ('3', 'Efectivo'), ('4', 'Credit')], default='0', max_length=1, null=True, verbose_name='Method of payment')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('idAttendant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quote_idAttendand', to=settings.AUTH_USER_MODEL)),
                ('idClient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_cliente', to='clientes.cliente')),
                ('idTin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_idTin', to='cuentas.tin')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuoteTraking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('event', models.CharField(choices=[('0', 'Recibido'), ('1', 'Respondido'), ('2', 'Aprobado'), ('3', 'Rechazado')], default='0', max_length=1, verbose_name='Recibido')),
                ('idTrafoQuote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trakingQuote', to='quotes.trafoquote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trafos',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('KVA', models.CharField(blank=True, choices=[('0', '15'), ('1', '30'), ('2', '75'), ('3', '100'), ('4', '167'), ('5', '200'), ('6', '250'), ('7', '400'), ('8', '500'), ('9', '600'), ('10', '750'), ('11', '1000'), ('12', '1500'), ('13', '2000')], max_length=2, null=True, verbose_name='kVA CAPACITY')),
                ('HVTAP', models.CharField(blank=True, choices=[('0', 'K-Tap - HV'), ('1', 'Fix HV')], max_length=2, null=True, verbose_name='HV TAP')),
                ('KTapHV', models.CharField(blank=True, choices=[('0', '12700/7200'), ('1', '24940/14400')], max_length=2, null=True, verbose_name='K Tap HV')),
                ('FIXHV', models.CharField(blank=True, choices=[('0', '7200'), ('1', '12470'), ('2', '22900')], max_length=2, null=True, verbose_name='FIX HV')),
                ('LV', models.CharField(blank=True, choices=[('0', '120/240'), ('1', '277/480')], max_length=2, null=True, verbose_name='LV')),
                ('HZ', models.CharField(blank=True, choices=[('0', '50'), ('1', '60')], max_length=2, null=True, verbose_name='HZ')),
                ('TYPE', models.CharField(blank=True, choices=[('0', 'Mono-phasic'), ('1', 'Three-phasic')], max_length=2, null=True, verbose_name='TYPE')),
                ('MOUNTING', models.CharField(blank=True, choices=[('0', 'Pole'), ('1', 'Standard'), ('2', 'Feed Through Pad')], max_length=2, null=True, verbose_name='MOUNTING TYPE')),
                ('COOLING', models.CharField(blank=True, choices=[('0', 'Oil'), ('1', 'Dry')], max_length=2, null=True, verbose_name='COOLING')),
                ('WINDING', models.CharField(blank=True, choices=[('0', 'Al - Al'), ('1', 'Cu - CU')], max_length=2, null=True, verbose_name='WINDING')),
                ('INSULAT', models.CharField(blank=True, choices=[('0', 'A'), ('1', 'E'), ('2', 'H')], max_length=2, null=True, verbose_name='INSULAT CLASS')),
                ('CONNECTION', models.CharField(blank=True, choices=[('0', 'WEY'), ('1', 'DELTA')], max_length=2, null=True, verbose_name='CONNECTION')),
                ('STANDARD', models.CharField(blank=True, choices=[('0', 'NMX-116'), ('1', 'IEC 61558')], max_length=2, null=True, verbose_name='STANDARD')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Cantidad')),
                ('unitCost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Costo unitario')),
                ('idTrafoQuote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trafo_Quote', to='quotes.trafoquote')),
            ],
            options={
                'verbose_name': 'Trafos',
                'verbose_name_plural': 'Trafos',
            },
        ),
    ]
