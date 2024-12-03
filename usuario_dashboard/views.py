from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from agente_dashboard.models import *
from usuario_dashboard.models import *
from usuario_dashboard.forms import RegistroReciclajeForm
from django.db.models import Sum
from django.db.models import Q
from django.db.models import Sum,Count
from .models import Cupon, Canje
@login_required
def inicio_usuario(request):
    eventos = Evento.objects.all().order_by('fecha')[:3]
    return render(request, 'usuario_dashboard/inicio_usuario.html', {'eventos': eventos})


@login_required
def reciclar(request):
    if request.method == 'POST':
        form = RegistroReciclajeForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            material = registro.material
            registro.puntos_obtenidos = material.puntos_por_kg * registro.cantidad
            registro.save()
            
            if request.user.es_usuario_comun:
                request.user.puntos += registro.puntos_obtenidos
                request.user.save()
            
            messages.success(request, 'Reciclaje registrado exitosamente.')
            return redirect('inicio_usuario')
    else:
        form = RegistroReciclajeForm()
    return render(request, 'usuario_dashboard/reciclar.html', {'form': form})




@login_required
def historial_canje(request):
    canjes = Canje.objects.filter(usuario=request.user).order_by('-fecha')
    
    total_canjes = canjes.count()
    total_puntos_gastados = canjes.aggregate(Sum('puntos_gastados'))['puntos_gastados__sum'] or 0
    total_puntos_otorgados = sum(canje.cupon.puntos_otorgados for canje in canjes)
    
    context = {
        'canjes': canjes,
        'total_canjes': total_canjes,
        'total_puntos_gastados': total_puntos_gastados,
        'total_puntos_otorgados': total_puntos_otorgados,
    }
    
    return render(request, 'usuario_dashboard/historial_canjes.html', context)

@login_required
def historial_reciclaje(request):
    # Change the context variable name to match what's expected in the template
    registros_reciclaje = RegistroReciclaje.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Add the statistics data needed by the template
    total_reciclajes = registros_reciclaje.count()
    total_puntos_obtenidos = registros_reciclaje.aggregate(Sum('puntos_obtenidos'))['puntos_obtenidos__sum'] or 0
    
    context = {
        'registros_reciclaje': registros_reciclaje,
        'total_reciclajes': total_reciclajes,
        'total_puntos_obtenidos': total_puntos_obtenidos
    }
    return render(request, 'usuario_dashboard/historial_reciclaje.html', context)


def simular_reciclaje(request):
    if request.method == 'POST':
        # Datos simulados fijos
        modulo = Modulo.objects.first()  # Asumimos que existe al menos un módulo
        material = Material.objects.get(nombre='Plástico')  # Asumimos que existe el material Plástico
        cantidad = 2.5  # Cantidad fija para la simulación
        puntos_obtenidos = 50  # Puntos fijos para la simulación

        if modulo.capacidad_actual + cantidad <= modulo.capacidad_total:
            # Crear el registro de reciclaje
            RegistroReciclaje.objects.create(
                usuario=request.user,
                modulo=modulo,
                material=material,
                cantidad=cantidad,
                puntos_obtenidos=puntos_obtenidos
            )

            # Actualizar puntos del usuario
            request.user.puntos += puntos_obtenidos
            request.user.save()

            # Actualizar capacidad del módulo
            modulo.capacidad_actual += cantidad
            if modulo.capacidad_actual >= modulo.capacidad_total:
                modulo.estado = 'lleno'
            modulo.save()

            # Mensaje de éxito
            messages.success(request, f'¡Has reciclado {cantidad} kg de {material.nombre} y ganado {puntos_obtenidos} puntos!')
        else:
            # El módulo está lleno
            messages.error(request, 'No se puede reciclar: el módulo está lleno.')

        return redirect('inicio_usuario')

    return render(request, 'usuario_dashboard/reciclar.html')


def cupones(request):
    cupones = Cupon.objects.filter().order_by('puntos_requeridos')
    
    if request.method == 'POST':
        cupon_id = request.POST.get('cupon_id')
        cupon = get_object_or_404(Cupon, id=cupon_id)
        usuario_comun = request.user  # Usa directamente request.user

        if usuario_comun.puntos >= cupon.puntos_requeridos :
            # Crear el registro de canje
            Canje.objects.create(usuario=usuario_comun, cupon=cupon, puntos_gastados=cupon.puntos_requeridos)
    
            # Actualizar puntos del usuario
            usuario_comun.puntos -= cupon.puntos_requeridos
            usuario_comun.save()
            
            
            # Mensaje de éxito
            messages.success(request, f'Has canjeado exitosamente el cupón: {cupon.nombre}')
        else:
            # Mensaje de error
            messages.error(request, 'No tienes suficientes puntos o el cupón no está disponible.')
        
        return redirect('cupones')  # Redirigir a la misma página
    
    return render(request, 'usuario_dashboard/cupones.html', {'cupones': cupones})

@login_required
def ver_voucher(request, canje_id):
    canje = get_object_or_404(Canje, id=canje_id)
    return render(request, 'usuario_dashboard/voucher.html', {
        'canje': canje
    })

@login_required
def guia_usuario(request):
    return render(request, 'usuario_dashboard/guia_usuario.html')

@login_required
def guia_modulos(request):
    return render(request, 'usuario_dashboard/guia_modulos.html')

@login_required
def tipos_residuos(request):
    return render(request, 'usuario_dashboard/tipos_residuos.html')

@login_required
def faqs(request):
    return render(request, 'usuario_dashboard/faqs.html')

@login_required
def educacion_ambiental(request):
    return render(request, 'usuario_dashboard/educacion_ambiental.html')

#ver si va en el agente?

@login_required
def historial_canjes(request):
    # Obtener todos los canjes del usuario
    canjes = Canje.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Calcular totales usando agregación
    totales = canjes.aggregate(
        total_puntos=Sum('puntos_gastados'),
        total_canjes=Count('id')
    )
    
    context = {
        'canjes': canjes,
        'total_canjes': totales['total_canjes'] or 0,
        'total_puntos_gastados': totales['total_puntos'] or 0
    }
    return render(request, 'usuario_dashboard/historial_canjes.html', context)
