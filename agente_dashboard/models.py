from django.conf import settings  # Importa settings para AUTH_USER_MODEL
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Modulo(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('mantenimiento', 'En Mantenimiento'),
        ('lleno', 'Lleno'),
    ]

    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    direccion_detallada = models.TextField(blank=True)
    capacidad_total = models.FloatField(validators=[MinValueValidator(0.0)])
    capacidad_actual = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    imagen = models.ImageField(upload_to='modulos/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible')
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    horario = models.CharField(max_length=200, default="24/7")

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return self.nombre

    def porcentaje_lleno(self):
        return min((self.capacidad_actual / self.capacidad_total) * 100, 100)
    
    def esta_disponible(self):
        return self.estado == 'disponible' and self.porcentaje_lleno() < 90

    def get_estado_display_class(self):
        return {
            'disponible': 'success',
            'mantenimiento': 'warning',
            'lleno': 'danger'
        }.get(self.estado, '')

class Cupon(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    puntos_requeridos = models.IntegerField()
    puntos_otorgados = models.IntegerField()  # New field for reward points
    
    def __str__(self):
        return self.nombre

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    puntos_por_kg = models.IntegerField()

    def __str__(self):
        return self.nombre

class Alerta(models.Model):
    TIPO_CHOICES = [
        ('mantenimiento', 'Mantenimiento'),
        ('lleno', 'Módulo Lleno'),
        ('danio', 'Daño Reportado'),
    ]
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='alertas')
    agente_asignado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Cambiado aquí

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.modulo.nombre}"

