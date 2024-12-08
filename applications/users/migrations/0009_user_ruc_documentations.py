# Generated by Django 5.0.6 on 2024-11-12 10:17

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ruc',
            field=models.CharField(blank=True, null=True, verbose_name='RUC'),
        ),
        migrations.CreateModel(
            name='Documentations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('typeDoc', models.CharField(choices=[('0', 'Contrato'), ('1', 'CV'), ('2', 'Informe Mensual'), ('3', 'Memorandum'), ('4', 'Oficio'), ('5', 'Carta'), ('6', 'Otro')], max_length=1, verbose_name='Tipo de dpcumento')),
                ('sumary', models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='Resumen')),
                ('doc_file', models.FileField(blank=True, null=True, upload_to='doc_pdfs/')),
                ('idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Documento de personal',
                'verbose_name_plural': 'Documentos de personal',
            },
        ),
    ]
