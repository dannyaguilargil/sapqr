from django.contrib import admin
from .models import  QR, colaborador
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.urls import reverse


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



class QRAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'activo', 'fecha_creacion', 'ver_qr')
    list_filter = ('activo',)

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

class Colaborador(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'fecha_registro')
    list_filter = ('marca',)
admin.site.register(colaborador, Colaborador)
