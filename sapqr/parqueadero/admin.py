from django.contrib import admin
from .models import  QR, colaborador
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
# Register your models here.
admin.site.register(Session)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'user')
    search_fields = ('object_repr', 'change_message')
admin.site.register(LogEntry, LogEntryAdmin)


class QRAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
admin.site.register(QR, QRAdmin)

class Colaborador(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'fecha_registro')
    list_filter = ('marca',)
admin.site.register(colaborador, Colaborador)
