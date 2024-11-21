from django.db import models
from django.utils.timezone import now

class Region(models.Model):
    nombre_region = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nombre_region

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class TipoInmueble(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class Direccion(models.Model):
    ubicacion = models.CharField(max_length=200)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return self.ubicacion


class Caracteristicas(models.Model):
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()


class Inmueble(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    caracteristicas = models.OneToOneField(Caracteristicas, on_delete=models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=now, editable=False)
    ultima_modificacion = models.DateTimeField(default=now)

    def __str__(self):
        return self.nombre
