# Generated by Django 5.0.6 on 2024-07-15 14:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0003_alter_projects_workers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='commissions',
            name='workers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
