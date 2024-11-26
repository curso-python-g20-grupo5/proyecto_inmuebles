from django.contrib import admin
from django.utils.timezone import now
from .models import Region, Comuna, TipoInmueble, Direccion, Caracteristicas, Inmueble


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_region")  # Mostrar columnas en la lista
    search_fields = ("nombre_region",)  # Barra de búsqueda
    ordering = ("nombre_region",)  # Ordenar por este campo


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "nombre_region")
    search_fields = ("nombre",)
    list_filter = ("nombre_region",)  # Filtro lateral por región


@admin.register(TipoInmueble)
class TipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo")
    search_fields = ("tipo",)


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ("id", "ubicacion", "comuna")
    search_fields = ("ubicacion",)
    list_filter = ("comuna",)


@admin.register(Caracteristicas)
class CaracteristicasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "m2_construidos",
        "m2_totales",
        "estacionamientos",
        "habitaciones",
        "banos",
    )
    list_editable = (
        "m2_construidos",
        "m2_totales",
        "estacionamientos",
        "habitaciones",
        "banos",
    )  # Permite editar en línea


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "direccion",
        "tipo_inmueble",
        "precio_mensual",
        "fecha_creacion",
        "ultima_modificacion",
    )
    search_fields = ("nombre", "descripcion")
    list_filter = ("tipo_inmueble", "direccion__comuna")
    ordering = ("precio_mensual",)
    readonly_fields = ("fecha_creacion", "ultima_modificacion")

    def save_model(self, request, obj, form, change):
        if change:
            obj.ultima_modificacion = now()
        super().save_model(request, obj, form, change)
