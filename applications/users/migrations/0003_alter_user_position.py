# Generated by Django 5.0.6 on 2025-07-12 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, choices=[('0', 'Administrador'), ('1', 'Compras'), ('2', 'Ventas'), ('3', 'Producción'), ('4', 'Gerencia'), ('5', 'Logística'), ('6', 'Recursos humanos'), ('7', 'Consultor externo'), ('8', 'Contabilidad'), ('9', 'TI')], max_length=1, verbose_name='Tipo de usuario'),
        ),
    ]
