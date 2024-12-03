from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'estado', 'modulo', 'agente_asignado', 'fecha_creacion')
    list_filter = ('tipo', 'estado', 'fecha_creacion')
    search_fields = ('descripcion', 'modulo__nombre', 'agente_asignado__username')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('tipo', 'descripcion', 'estado', 'fecha_creacion')
        }),
        ('Información del Módulo', {
            'fields': ('modulo',)
        }),
        ('Asignación', {
            'fields': ('agente_asignado',)
        }),
    )

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos_por_kg')


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos_requeridos', 'puntos_otorgados')
    search_fields = ('nombre', 'descripcion')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'ubicacion')
    list_filter = ('fecha',)
    search_fields = ('titulo', 'descripcion')


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'porcentaje_lleno', 'estado', 'ultima_actualizacion')
    list_filter = ('estado',)
    search_fields = ('nombre', 'ubicacion', 'direccion_detallada')
    readonly_fields = ('ultima_actualizacion',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'ubicacion', 'direccion_detallada', 'horario')
        }),
        ('Capacidad', {
            'fields': ('capacidad_total', 'capacidad_actual')
        }),
        ('Ubicación', {
            'fields': ('latitud', 'longitud')
        }),
        ('Estado', {
            'fields': ('estado', 'ultima_actualizacion', 'imagen')
        }),
    )

    def porcentaje_lleno(self, obj):
        return f"{obj.porcentaje_lleno():.2f}%"
    porcentaje_lleno.short_description = "Porcentaje Lleno"