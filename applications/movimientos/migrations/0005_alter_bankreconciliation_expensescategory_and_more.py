# Generated by Django 5.0.6 on 2024-07-18 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0004_alter_bankreconciliation_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankreconciliation',
            name='expensesCategory',
            field=models.CharField(blank=True, choices=[('0', 'compras'), ('1', 'servicio'), ('2', 'proveedor'), ('3', 'impuestos'), ('4', 'caja chica'), ('5', 'comisiones'), ('6', 'proyecto'), ('7', 'planilla'), ('8', 'operaciones'), ('9', 'multas'), ('10', 'personal'), ('11', 'transferencias internas'), ('12', 'agente aduanas'), ('13', 'prestamo')], max_length=2, null=True, verbose_name='Categoria de egresos'),
        ),
        migrations.AlterField(
            model_name='bankreconciliation',
            name='incomeCategory',
            field=models.CharField(blank=True, choices=[('0', 'abono pedido'), ('1', 'venta'), ('2', 'alquiler'), ('3', 'donacion'), ('4', 'suscripcion'), ('5', 'prestamo'), ('6', 'Transferencia interna')], max_length=1, null=True, verbose_name='Categoria de ingresos'),
        ),
        migrations.AlterField(
            model_name='bankreconciliation',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='conciliaciones_pdfs/'),
        ),
        migrations.AlterField(
            model_name='bankreconciliation',
            name='subCategoryPallRoy',
            field=models.CharField(blank=True, choices=[('0', 'remuneracion'), ('1', 'AFP'), ('2', 'CTS'), ('3', 'seguros'), ('4', 'bono'), ('5', 'otro')], max_length=1, null=True, verbose_name='Sub Categoria planilla'),
        ),
    ]