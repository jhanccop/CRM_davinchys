# Generated by Django 5.0.6 on 2024-08-17 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0019_alter_dailytasks_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailytasks',
            old_name='type',
            new_name='is_overTime',
        ),
    ]
