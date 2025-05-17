from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class QR(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    imagen_qr = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def generar_qr(self):
        # Crear la URL de la vista de registro con el uuid
        url = f'http://192.168.162.49:8000/registro/{self.uuid}/'  # Cambia 'tusitio.com' por tu dominio
        qr_img = qrcode.make(url)  # Generar el QR con la URL

        # Guardar la imagen QR generada
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        filename = f'qr_{self.uuid}.png'
        self.imagen_qr.save(filename, File(buffer), save=False)
        buffer.close()

    def save(self, *args, **kwargs):
        # Genera el QR solo si no existe ya
        if not self.imagen_qr:
            self.generar_qr()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)
    

class colaborador(models.Model):
    qr = models.ForeignKey(QR, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre completo")
    dependencia = models.CharField(max_length=100, verbose_name="Area o dependencia")
    marca = models.CharField(max_length=50, verbose_name="Marca del vehiculo")
    modelo = models.CharField(max_length=50, verbose_name="Modelo del vehiculo")
    placa = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nombre_completo)

class RegistroVehiculo(models.Model):
    qr = models.ForeignKey(QR, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.placa


class MovimientoVehiculo(models.Model):
    registro = models.ForeignKey(RegistroVehiculo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=(('entrada', 'Entrada'), ('salida', 'Salida')))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creaccion")

    def __str__(self):
        return f"{self.registro.placa} - {self.tipo} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"