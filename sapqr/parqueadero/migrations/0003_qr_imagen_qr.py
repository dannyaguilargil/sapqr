# Generated by Django 5.2.1 on 2025-05-17 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueadero', '0002_alter_qr_fecha_creacion_colaborador'),
    ]

    operations = [
        migrations.AddField(
            model_name='qr',
            name='imagen_qr',
            field=models.ImageField(blank=True, null=True, upload_to='qr/'),
        ),
    ]
