# Generated by Django 5.0.6 on 2024-07-15 13:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='workers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]