# Generated by Django 5.0.6 on 2024-07-16 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0003_bankreconciliation_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankreconciliation',
            name='pdf_file',
            field=models.FileField(null=True, upload_to='conciliaciones_pdfs/'),
        ),
    ]