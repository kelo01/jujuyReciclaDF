from django.db import models

from django.db import models
from core.models import UsuarioComun

from agente_dashboard.models import *


class RegistroReciclaje(models.Model):
    usuario = models.ForeignKey(UsuarioComun, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    puntos_obtenidos = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.cantidad}kg de {self.material.nombre} en {self.modulo.nombre}"

class Canje(models.Model):
    usuario = models.ForeignKey(UsuarioComun, on_delete=models.CASCADE)
    cupon = models.ForeignKey(Cupon, on_delete=models.CASCADE)
    puntos_gastados = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.cupon.nombre}"

    @property
    def puntos_requeridos(self):
        return self.cupon.puntos_requeridos

    @property
    def puntos_otorgados(self):
        return self.cupon.puntos_otorgados