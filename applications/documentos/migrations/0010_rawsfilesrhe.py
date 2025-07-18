# Generated by Django 5.0.6 on 2025-06-03 23:25

import django.core.validators
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0009_alter_financialdocuments_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawsFilesRHE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('archivo', models.FileField(upload_to='uploads/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])])),
                ('procesado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Archivo Original',
                'verbose_name_plural': 'Archivos Originales',
            },
        ),
    ]
