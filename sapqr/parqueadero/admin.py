from django.contrib import admin
from .models import  QR, colaborador, RegistroVehiculo, MovimientoVehiculo
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ExportMixin
from import_export import resources


admin.site.site_header = "Parquedadero con QR v.0.1 @d4n7.dev©"
admin.site.site_title = "SAP QR - @d4n7.dev "
admin.site.index_title = "Administracion de parqueadero"

# Register your models here.
admin.site.register(Session)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'user')
    search_fields = ('object_repr', 'change_message')
admin.site.register(LogEntry, LogEntryAdmin)

class qrResource(resources.ModelResource):
    class Meta:
        model = QR

class QRAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = qrResource
    list_display = ('uuid', 'activo', 'fecha_creacion', 'ver_qr')
    list_filter = ('activo',)  # Agrega filtro para el campo 'activo'
    def ver_qr(self, obj):
        if obj.imagen_qr:
            return format_html(
                '<img src="{}" width="100" height="100"/><br>'  
                '<a href="{}" download>Descargar</a> | '  
                '<a href="{}" target="_blank">Imprimir</a>',  
                obj.imagen_qr.url,  
                obj.imagen_qr.url, 
                obj.imagen_qr.url  
            )
        return "QR no generado" 

    ver_qr.short_description = "QR"

admin.site.register(QR, QRAdmin)

# Crear el recurso para import/export
class ColaboradorResource(resources.ModelResource):
    class Meta:
        model = colaborador

class Colaborador(ExportMixin, admin.ModelAdmin):
    resource_class = ColaboradorResource
    list_display = ('id', 'nombre_completo', 'fecha_registro')
    list_filter = ('marca',)
admin.site.register(colaborador, Colaborador)

class rvResource(resources.ModelResource):
    class Meta:
        model = RegistroVehiculo

class Registro_vehiculo(ExportMixin, admin.ModelAdmin):
    resource_class = rvResource
    list_display = ('qr', 'placa', 'fecha_registro')
    list_filter = ('placa',)
admin.site.register(RegistroVehiculo, Registro_vehiculo)

class mvResource(resources.ModelResource):
    class Meta:
        model = MovimientoVehiculo

class Evento(ExportMixin, admin.ModelAdmin):
    resource_class = mvResource
    list_display = ('registro', 'tipo', 'timestamp')
    list_filter = ('tipo',)
admin.site.register(MovimientoVehiculo, Evento)
