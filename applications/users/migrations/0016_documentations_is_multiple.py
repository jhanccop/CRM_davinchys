# Generated by Django 5.0.6 on 2024-11-18 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_documentations_typedoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentations',
            name='is_multiple',
            field=models.BooleanField(default=False),
        ),
    ]
