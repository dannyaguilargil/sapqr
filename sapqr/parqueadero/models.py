from django.db import models
import uuid

class QR(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uuid)
    

class colaborador(models.Model):
    qr = models.ForeignKey(QR, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre completo")
    dependencia = models.CharField(max_length=100, verbose_name="Area o dependencia")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nombre_completo)
