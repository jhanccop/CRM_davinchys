# Generated by Django 5.0.6 on 2024-09-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_condition_user_gender_user_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cv_file',
            field=models.FileField(blank=True, null=True, upload_to='cv_pdfs/'),
        ),
    ]
