from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioComun

class UsuarioComunAdmin(UserAdmin):
    list_display = ('username', 'email', 'dni', 'telefono','puntos', 'edad', 'rol', 'zona_asignada', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'dni')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('email', 'dni', 'telefono', 'direccion', 'edad', 'rol', 'zona_asignada')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'dni', 'telefono', 'direccion', 'edad', 'rol', 'zona_asignada'),
        }),
    )
    ordering = ('date_joined',)

admin.site.register(UsuarioComun, UsuarioComunAdmin)