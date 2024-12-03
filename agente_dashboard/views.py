from django.shortcuts import render
from django.db.models import Q
from agente_dashboard.models import *
from usuario_dashboard.models import *
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def lista_modulos(request):
    query = request.GET.get('q', '')
    modulos = Modulo.objects.all()
    
    if query:
        modulos = modulos.filter(
            Q(nombre__icontains=query) |
            Q(ubicacion__icontains=query) |
            Q(direccion_detallada__icontains=query)
        )
    
    modulos_disponibles = modulos.filter(estado='disponible')
    modulos_otros = modulos.exclude(estado='disponible')
    
    modulos_data = [
        {
            'nombre': m.nombre,
            'ubicacion': m.ubicacion,
            'latitud': float(m.latitud),
            'longitud': float(m.longitud),
            'estado': m.estado,
            'porcentaje_lleno': m.porcentaje_lleno()
        }
        for m in modulos
    ]
    
    context = {
        'modulos_disponibles': modulos_disponibles,
        'modulos_otros': modulos_otros,
        'query': query,
        'modulos_json': json.dumps(modulos_data)
    }
    return render(request, 'usuario_dashboard/lista_modulos.html', context)


def lista_modulosA(request):
    query = request.GET.get('q', '')
    modulos = Modulo.objects.all()
    
    if query:
        modulos = modulos.filter(
            Q(nombre__icontains=query) |
            Q(ubicacion__icontains=query) |
            Q(direccion_detallada__icontains=query)
        )
    
    modulos_disponibles = modulos.filter(estado='disponible')
    modulos_otros = modulos.exclude(estado='disponible')
    
    modulos_data = [
        {
            'nombre': m.nombre,
            'ubicacion': m.ubicacion,
            'latitud': float(m.latitud),
            'longitud': float(m.longitud),
            'estado': m.estado,
            'porcentaje_lleno': m.porcentaje_lleno()
        }
        for m in modulos
    ]
    
    context = {
        'modulos_disponibles': modulos_disponibles,
        'modulos_otros': modulos_otros,
        'query': query,
        'modulos_json': json.dumps(modulos_data)
    }
    return render(request, 'agente_dashboard/lista_modulosA.html', context)


def mapa_modulos(request):
    modulos = Modulo.objects.all()
    modulos_data = [
        {
            'nombre': m.nombre,
            'ubicacion': m.ubicacion,
            'latitud': float(m.latitud),
            'longitud': float(m.longitud),
            'estado': m.estado,
            'porcentaje_lleno': m.porcentaje_lleno()
        }
        for m in modulos
    ]
    
    context = {
        'modulos_json': json.dumps(modulos_data)
    }
    return render(request, 'usuario_dashboard/mapa_modulos.html', context)

def mapa_modulosA(request):
    modulos = Modulo.objects.all()
    modulos_data = [
        {
            'nombre': m.nombre,
            'ubicacion': m.ubicacion,
            'latitud': float(m.latitud),
            'longitud': float(m.longitud),
            'estado': m.estado,
            'porcentaje_lleno': m.porcentaje_lleno()
        }
        for m in modulos
    ]
    
    context = {
        'modulos_json': json.dumps(modulos_data)
    }
    return render(request, 'agente_dashboard/mapa_modulosA.html', context)


def es_agente(user):
    return user.is_authenticated and user.rol == 'agente'

@login_required
@user_passes_test(es_agente)
def inicio_agente(request):
    # Obtener módulos asignados al agente
    modulos = Modulo.objects.all()
    
    # Obtener alertas activas
    alertas_activas = Alerta.objects.filter(estado='activa').count()
    
    
    reciclado_actual = Modulo.objects.aggregate(total=Sum('capacidad_actual'))['total'] or 0
    
    context = {
        'modulos': modulos,
        'alertas_activas': alertas_activas,
        'reciclado_hoy': reciclado_actual,
    }
    
    return render(request, 'agente_dashboard/inicio_agente.html', context)


@login_required
@user_passes_test(es_agente)
def estadisticas(request):
    return render(request, 'agente_dashboard/estadisticas.html')


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Alerta, Modulo
import json

def es_agente(user):
    return user.is_authenticated and user.rol == 'agente'

@login_required
@user_passes_test(es_agente)
def gestion_alertas(request):
    # Obtener todas las alertas activas y en proceso
    alertas_db = Alerta.objects.exclude(estado='resuelta').order_by('-fecha_creacion')
    
    # Verificar módulos y crear alertas automáticas
    modulos = Modulo.objects.all()
    for modulo in modulos:
        if modulo.estado == 'mantenimiento':
            Alerta.objects.get_or_create(
                tipo='mantenimiento',
                modulo=modulo,
                defaults={
                    'descripcion': f"El módulo {modulo.nombre} requiere mantenimiento.",
                    'estado': 'activa'
                }
            )
        elif modulo.porcentaje_lleno() >= 90:
            Alerta.objects.get_or_create(
                tipo='lleno',
                modulo=modulo,
                defaults={
                    'descripcion': f"El módulo {modulo.nombre} está casi lleno ({modulo.porcentaje_lleno()}%).",
                    'estado': 'activa'
                }
            )
    
    # Actualizar queryset después de crear nuevas alertas
    alertas_db = Alerta.objects.exclude(estado='resuelta').order_by('-fecha_creacion')
    
    alertas_data = []
    for alerta in alertas_db:
        alertas_data.append({
            'id': alerta.id,
            'tipo': alerta.tipo,
            'descripcion': alerta.descripcion,
            'fecha_creacion': alerta.fecha_creacion.isoformat(),
            'estado': alerta.estado,
            'modulo': {
                'id': alerta.modulo.id,
                'nombre': alerta.modulo.nombre
            } if alerta.modulo else None
        })

    context = {
        'alertas_json': json.dumps(alertas_data),
        'estados_json': json.dumps(dict(Alerta.ESTADO_CHOICES)),
        'tipos_json': json.dumps(dict(Alerta.TIPO_CHOICES)),
    }
    return render(request, 'agente_dashboard/gestion_alertas.html', context)

@require_POST
@login_required
@user_passes_test(es_agente)
def atender_alerta(request, alerta_id):
    alerta = get_object_or_404(Alerta, id=alerta_id)
    
    if alerta.estado == 'activa':
        alerta.estado = 'en_proceso'
        alerta.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Alerta atendida correctamente'
        })
    return JsonResponse({
        'status': 'error',
        'message': 'La alerta no puede ser atendida'
    }, status=400)

@require_POST
@login_required
@user_passes_test(es_agente)
def resolver_alerta(request, alerta_id):
    alerta = get_object_or_404(Alerta, id=alerta_id)
    
    if alerta.estado == 'en_proceso':
        alerta.estado = 'resuelta'
        alerta.fecha_resolucion = timezone.now()
        alerta.save()

        # Actualizar estado del módulo
        if alerta.modulo:
            if alerta.tipo == 'lleno':
                alerta.modulo.capacidad_actual = 0
                alerta.modulo.estado = 'disponible'
            elif alerta.tipo == 'mantenimiento':
                alerta.modulo.estado = 'disponible'
            alerta.modulo.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Alerta resuelta correctamente'
        })
    return JsonResponse({
        'status': 'error',
        'message': 'La alerta no puede ser resuelta'
    }, status=400)
@login_required
@user_passes_test(es_agente)
def configuracion(request):
    return render(request, 'agente_dashboard/configuracion.html')