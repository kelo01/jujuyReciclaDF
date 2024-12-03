from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioComun(AbstractUser):
    ROL_CHOICES = [
        ('usuario', 'Usuario Común'),
        ('agente', 'Agente Ambiental'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario')
    dni = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    edad = models.IntegerField(null=True, blank=True)
    zona_asignada = models.CharField(max_length=100, blank=True, null=True)  # Solo para agentes
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return self.username



