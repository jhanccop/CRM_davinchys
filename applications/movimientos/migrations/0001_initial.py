# Generated by Django 5.0.6 on 2024-07-10 13:21

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actividades', '0001_initial'),
        ('clientes', '0001_initial'),
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentsUploaded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fileName', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de archivo')),
                ('observations', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observaciones')),
            ],
            options={
                'verbose_name': 'Documento subido',
                'verbose_name_plural': 'Documentos subidos',
            },
        ),
        migrations.CreateModel(
            name='InternalTransfers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('SourceAmount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto origen')),
                ('DestinationAmount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto destino')),
                ('opNumber', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero de operacion')),
            ],
            options={
                'verbose_name': 'Transferencia',
                'verbose_name_plural': 'Transferencias',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('dateTime', models.DateTimeField(verbose_name='Fecha de movimiento')),
                ('category', models.CharField(blank=True, choices=[('0', 'remuneracion'), ('1', 'proveedor'), ('2', 'servicio'), ('3', 'comision'), ('4', 'compra'), ('5', 'impuestos'), ('6', 'caja chica'), ('7', 'Transferencia interna'), ('8', 'abono pedido'), ('9', 'venta'), ('10', 'alquiler'), ('11', 'donacion'), ('12', 'suscripcion'), ('13', 'prestamo')], max_length=20, verbose_name='Categoria')),
                ('idTransaction', models.CharField(blank=True, max_length=100, null=True, verbose_name='IdMovimiento')),
                ('transactionName', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de movimiento')),
                ('clientName', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de receptor')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('currency', models.CharField(blank=True, choices=[('0', 'Soles'), ('1', 'Dolares')], max_length=20, verbose_name='Tipo de moneda')),
                ('transactionType', models.CharField(blank=True, choices=[('0', 'egreso'), ('1', 'ingreso')], max_length=20, verbose_name='Tipo de movimiento')),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Saldo')),
            ],
            options={
                'verbose_name': 'Movimiento',
                'verbose_name_plural': 'Movimientos',
            },
        ),
        migrations.CreateModel(
            name='BankMovements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField(verbose_name='Fecha y hora')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripción EEC')),
                ('transactionType', models.CharField(blank=True, choices=[('0', 'egreso'), ('1', 'ingreso')], max_length=1, verbose_name='Tipo de movimiento')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='saldo')),
                ('amountReconcilied', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto conciliado')),
                ('opNumber', models.CharField(blank=True, max_length=10, null=True, verbose_name='Numero de operacion')),
                ('idAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cuentas.account')),
            ],
            options={
                'verbose_name': 'Movimiento bancario',
                'verbose_name_plural': 'Movimientos bancarios',
            },
        ),
        migrations.CreateModel(
            name='BankReconciliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Fecha de emisión')),
                ('typeInvoice', models.CharField(blank=True, choices=[('0', 'Factura'), ('1', 'RHE'), ('2', 'PL'), ('3', 'Comprobante Davinchys'), ('4', 'NC')], max_length=1, null=True, verbose_name='Tipo de comprobante')),
                ('idInvoice', models.CharField(blank=True, max_length=25, null=True, verbose_name='Id de comprobante')),
                ('ActivitiesCategory', models.CharField(blank=True, choices=[('0', 'pedidos trafos'), ('1', 'comision'), ('2', 'proyecto')], max_length=10, null=True, verbose_name='Categoria de actividades')),
                ('expensesCategory', models.CharField(blank=True, choices=[('0', 'compras'), ('1', 'servicio'), ('2', 'proveedor'), ('3', 'impuestos'), ('4', 'caja chica'), ('5', 'comisiones'), ('6', 'proyecto'), ('7', 'planilla'), ('8', 'operaciones'), ('9', 'multas'), ('10', 'personal'), ('11', 'transferencias internas'), ('12', 'agente aduanas'), ('13', 'prestamo')], max_length=20, verbose_name='Categoria de egresos')),
                ('incomeCategory', models.CharField(blank=True, choices=[('0', 'abono pedido'), ('1', 'venta'), ('2', 'alquiler'), ('3', 'donacion'), ('4', 'suscripcion'), ('5', 'prestamo'), ('6', 'Transferencia interna')], max_length=20, verbose_name='Categoria de ingresos')),
                ('subCategoryPallRoy', models.CharField(blank=True, choices=[('0', 'remuneracion'), ('1', 'AFP'), ('2', 'CTS'), ('3', 'seguros'), ('4', 'bono'), ('5', 'otro')], max_length=20, null=True, verbose_name='Sub Categoria planilla')),
                ('subCategoryCashBox', models.CharField(blank=True, choices=[('0', 'movilidad'), ('1', 'oficina'), ('2', 'alimentacion'), ('3', 'limpieza'), ('4', 'repuestos'), ('5', 'personal'), ('6', 'otro')], max_length=2, null=True, verbose_name='Sub Categoria caja chica')),
                ('annotation', models.CharField(blank=True, choices=[('1', 'anticipo'), ('1', 'pago final'), ('2', 'total')], max_length=2, null=True, verbose_name='Anotaciones')),
                ('contabilidad', models.CharField(blank=True, choices=[('0', 'Agente de aduana'), ('1', 'Caja chica'), ('2', 'Caja General'), ('3', 'Caja General ventas'), ('4', 'RHE general'), ('5', 'Adicional'), ('6', 'Personal'), ('7', 'PL'), ('8', 'renta')], max_length=2, null=True, verbose_name='Sub Categoria contabilidad')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripción')),
                ('amountReconcilied', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto conciliado')),
                ('idBankMovements', models.ManyToManyField(blank=True, to='movimientos.bankmovements')),
                ('idClient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('idCommission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.commissions')),
                ('idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.projects')),
                ('idTrafoOrder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.trafoorder')),
            ],
            options={
                'verbose_name': 'Conciliación',
                'verbose_name_plural': 'Concicliaciones Bancarias',
            },
        ),
    ]
