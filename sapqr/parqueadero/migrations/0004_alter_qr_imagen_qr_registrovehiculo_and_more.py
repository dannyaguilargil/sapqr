# Generated by Django 5.2.1 on 2025-05-17 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueadero', '0003_qr_imagen_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr',
            name='imagen_qr',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.CreateModel(
            name='RegistroVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('qr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parqueadero.qr')),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaccion')),
                ('registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parqueadero.registrovehiculo')),
            ],
        ),
    ]
