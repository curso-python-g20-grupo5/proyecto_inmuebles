from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()


class Inmueble(models.Model):
    propietario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="propiedades"
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    caracteristicas = models.OneToOneField(Caracteristicas, on_delete=models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)
    precio_mensual = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ("arrendador", "Arrendador"),
        ("arrendatario", "Arrendatario"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="arrendatario"
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        # Get or create the profile if it doesn't exist
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Get or create the profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.save()


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    ]

    inmueble = models.ForeignKey(
        Inmueble, on_delete=models.CASCADE, related_name="reservas"
    )
    arrendatario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservas"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="pendiente"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.arrendatario.username} para {self.inmueble.nombre}"
