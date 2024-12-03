# Register your models here.
from django.contrib import admin
from .models import RegistroReciclaje,Canje 

@admin.register(RegistroReciclaje)
class RegistroReciclajeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'modulo', 'material', 'cantidad', 'puntos_obtenidos', 'fecha')
    list_filter = ('material', 'modulo', 'fecha')
    search_fields = ('usuario__username',)


@admin.register(Canje)
class CanjeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cupon', 'puntos_gastados', 'fecha')
    list_filter = ('cupon', 'fecha')
    search_fields = ('usuario__username',)

