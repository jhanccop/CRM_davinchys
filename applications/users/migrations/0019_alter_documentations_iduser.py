# Generated by Django 5.0.6 on 2024-12-03 16:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_documentations_iddoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentations',
            name='idUser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person', to=settings.AUTH_USER_MODEL),
        ),
    ]
