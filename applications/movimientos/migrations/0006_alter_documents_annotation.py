# Generated by Django 5.0.6 on 2025-01-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0005_documents_idtin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='annotation',
            field=models.CharField(blank=True, choices=[('0', 'anticipo'), ('1', 'pago final'), ('2', 'total')], max_length=2, null=True, verbose_name='Anotaciones'),
        ),
    ]
