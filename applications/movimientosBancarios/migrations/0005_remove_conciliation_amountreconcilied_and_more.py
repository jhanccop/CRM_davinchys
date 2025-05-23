# Generated by Django 5.0.6 on 2025-05-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientosBancarios', '0004_bankmovements_pdf_file_delete_bankvoucher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conciliation',
            name='amountReconcilied',
        ),
        migrations.RemoveField(
            model_name='conciliation',
            name='equivalentAmount',
        ),
        migrations.AddField(
            model_name='conciliation',
            name='amountEUR',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto EUR'),
        ),
        migrations.AddField(
            model_name='conciliation',
            name='amountPEN',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto PEN'),
        ),
        migrations.AddField(
            model_name='conciliation',
            name='amountUSD',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto USD'),
        ),
    ]
