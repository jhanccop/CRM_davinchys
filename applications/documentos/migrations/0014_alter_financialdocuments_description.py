# Generated by Django 5.0.6 on 2025-06-04 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0013_remove_financialdocuments_xlm_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialdocuments',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]
