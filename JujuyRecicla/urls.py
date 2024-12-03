from django.contrib import admin
from django.urls import path
from core import views as core_views
from usuario_dashboard import views as usuario_views
from agente_dashboard import views as agente_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', core_views.LoginView.as_view(), name='login'),
    path('registro/', core_views.RegistroView.as_view(), name='registro'),
    path('logout/', core_views.LogoutView.as_view(), name='logout'),


    #Agente
    path('inicio/Agente/',agente_views.inicio_agente, name='inicio_agente'),
    path('estadisticas/', agente_views.estadisticas, name='estadisticas'),

    path('alertas/', agente_views.gestion_alertas, name='gestion_alertas'),
    path('atender-alerta/<int:alerta_id>/', agente_views.atender_alerta, name='atender_alerta'),
    path('resolver-alerta/<int:alerta_id>/', agente_views.resolver_alerta, name='resolver_alerta'),

    path('perfil/editar/Agente', core_views.EditarPerfilAgenteView.as_view(), name='editar_perfil_agente'),
    path('configuracion/Agente', core_views.ConfiguracionAgenteView.as_view(), name='configuracion_agente'),


    #UsuarioComun

    path('inicio/EcoUser/', usuario_views.inicio_usuario, name='inicio_usuario'),

    path('reciclar/', usuario_views.simular_reciclaje, name='reciclar'),
    path('historial-reciclaje/', usuario_views.historial_reciclaje, name='historial_reciclaje'),
    path('historial-canjes/', usuario_views.historial_canjes, name='historial_canjes'),
    path('cupones/', usuario_views.cupones, name='cupones'),
    path('canjes/<int:canje_id>/voucher/', usuario_views.ver_voucher, name='ver_voucher'),
    path('guia-usuario/', usuario_views.guia_usuario, name='guia_usuario'),
    path('guia-modulos/', usuario_views.guia_modulos, name='guia_modulos'),
    path('tipos-residuos/', usuario_views.tipos_residuos, name='tipos_residuos'),
    path('faqs/', usuario_views.faqs, name='faqs'),
    path('educacion-ambiental/', usuario_views.educacion_ambiental, name='educacion_ambiental'),
    path('perfil/editar/EcoUser', core_views.EditarPerfilView.as_view(), name='editar_perfil_user'),
    path('configuracion/EcoUser', core_views.ConfiguracionView.as_view(), name='configuracion_user'),

    # Rutas para los módulos de reciclaje
    path('lista_modulos/', agente_views.lista_modulos, name='lista_modulos'),
    path('mapa/', agente_views.mapa_modulos, name='mapa_modulos'),

    path('lista_modulos/Agente', agente_views.lista_modulosA, name='lista_modulosA'),
    path('mapa/Agente/', agente_views.mapa_modulosA, name='mapa_modulosA'),


    path('admin/', admin.site.urls),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)