from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .forms import PropertySearchForm
from .models import Comuna
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import InmuebleForm, ReservaForm
from django.db import transaction
from .models import Inmueble, Reserva
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                "home"
            )  # Redirige a la página de inicio después del registro
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def home(request):
    return render(request, "home.html")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        "form": form,
        "user": request.user,
    }
    return render(request, "accounts/profile.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect("login")


def search_properties(request):
    form = PropertySearchForm(request.GET or None)
    properties = Inmueble.objects.all()

    if form.is_valid():
        region = form.cleaned_data.get("region")
        comuna = form.cleaned_data.get("comuna")
        tipo_inmueble = form.cleaned_data.get("tipo_inmueble")
        precio_min = form.cleaned_data.get("precio_min")
        precio_max = form.cleaned_data.get("precio_max")

        if region:
            properties = properties.filter(direccion__comuna__nombre_region=region)
        if comuna:
            properties = properties.filter(direccion__comuna=comuna)
        if tipo_inmueble:
            properties = properties.filter(tipo_inmueble=tipo_inmueble)
        if precio_min:
            properties = properties.filter(precio_mensual__gte=precio_min)
        if precio_max:
            properties = properties.filter(precio_mensual__lte=precio_max)

    context = {
        "form": form,
        "properties": properties,
    }
    return render(request, "search_properties.html", context)


def get_comunas(request):
    region_id = request.GET.get("region")
    comunas = Comuna.objects.filter(nombre_region_id=region_id).values("id", "nombre")
    return JsonResponse(list(comunas), safe=False)


@login_required
@transaction.atomic
def crear_propiedad(request):
    if request.user.profile.user_type != "arrendatario":
        messages.error(request, "Solo los arrendadores pueden crear propiedades.")
        return redirect("profile")

    if request.method == "POST":
        form = InmuebleForm(request.POST)
        if form.is_valid():
            try:
                propiedad = form.save(commit=True, user=request.user)
                messages.success(request, "Propiedad creada exitosamente.")
                return redirect("mis_propiedades")
            except Exception as e:
                messages.error(request, f"Error al crear la propiedad: {str(e)}")
    else:
        form = InmuebleForm()

    return render(request, "crear_propiedad.html", {"form": form})


@login_required
def editar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Inmueble, id=propiedad_id, propietario=request.user)
    if request.method == "POST":
        form = InmuebleForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            messages.success(request, "Propiedad actualizada exitosamente.")
            return redirect("mis_propiedades")
    else:
        form = InmuebleForm(instance=propiedad)
    return render(
        request, "editar_propiedad.html", {"form": form, "propiedad": propiedad}
    )


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(arrendatario=request.user)
    return render(request, "mis_reservas.html", {"reservas": reservas})


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, arrendatario=request.user)
    if request.method == "POST":
        reserva.estado = "cancelada"
        reserva.save()
        messages.success(request, "Reserva cancelada exitosamente.")
        return redirect("mis_reservas")
    return render(request, "cancelar_reserva.html", {"reserva": reserva})


# @login_required
def property_detail(request, pk):
    property = get_object_or_404(Inmueble, pk=pk)
    reserva = Reserva.objects.filter(inmueble=property, estado="confirmada").first()

    if request.method == "POST" and request.user.profile.user_type == "arrendador":
        form = ReservaForm(request.POST)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)
            nueva_reserva.inmueble = property
            nueva_reserva.arrendatario = request.user
            nueva_reserva.save()
            messages.success(request, "Reserva realizada con éxito.")
            return redirect("property_detail", pk=pk)
    else:
        form = ReservaForm()

    context = {
        "property": property,
        "form": form,
        "reserva": reserva,
    }
    return render(request, "property_detail.html", context)


@login_required
def eliminar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Inmueble, id=propiedad_id, propietario=request.user)
    if request.method == "POST":
        propiedad.delete()
        messages.success(request, "Propiedad eliminada exitosamente.")
        return redirect("mis_propiedades")
    return render(request, "eliminar_propiedad.html", {"propiedad": propiedad})


@login_required
def aceptar_arrendatario(request, reserva_id):
    reserva = get_object_or_404(
        Reserva, id=reserva_id, inmueble__propietario=request.user
    )
    if request.method == "POST":
        reserva.estado = "confirmada"
        reserva.save()
        messages.success(request, "Reserva aceptada exitosamente.")
        return redirect("mis_propiedades")
    return render(request, "aceptar_arrendatario.html", {"reserva": reserva})


@login_required
def mis_propiedades(request):
    propiedades = Inmueble.objects.filter(propietario=request.user).prefetch_related(
        "reservas"
    )
    return render(request, "mis_propiedades.html", {"propiedades": propiedades})


def landing_view(request):

    featured_properties = Inmueble.objects.all().order_by("-fecha_creacion")[:6]

    context = {
        "featured_properties": featured_properties,
    }
    return render(request, "landing.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("landing")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})
