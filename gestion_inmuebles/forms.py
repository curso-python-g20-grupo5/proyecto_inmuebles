from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Inmueble,
    Direccion,
    Caracteristicas,
    TipoInmueble,
    Comuna,
    Region,
    Reserva,
    Profile,
)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "user_type")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user_type = self.cleaned_data["user_type"]
            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = user_type
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, label="Apellido")
    email = forms.EmailField(required=True, label="Correo electrónico")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Biografía")
    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES, required=True, label="Tipo de usuario"
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_profile = self.instance.profile
                self.fields["bio"].initial = user_profile.bio
                self.fields["user_type"].initial = user_profile.user_type
            except Profile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.bio = self.cleaned_data["bio"]
        profile.user_type = self.cleaned_data["user_type"]
        profile.save()

        return user


class PropertySearchForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(), required=False, empty_label="Todas las regiones"
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(), required=False, empty_label="Todas las comunas"
    )
    tipo_inmueble = forms.ModelChoiceField(
        queryset=TipoInmueble.objects.all(),
        required=False,
        empty_label="Todos los tipos",
    )
    precio_min = forms.DecimalField(required=False, min_value=0)
    precio_max = forms.DecimalField(required=False, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["comuna"].queryset = Comuna.objects.filter(
                    nombre_region_id=region_id
                )
            except (ValueError, TypeError):
                self.fields["comuna"].queryset = Comuna.objects.all()
        else:
            self.fields["comuna"].queryset = Comuna.objects.all()


class InmuebleForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200, label="Nombre de la propiedad")
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    tipo_inmueble = forms.ModelChoiceField(
        queryset=TipoInmueble.objects.all(), label="Tipo de inmueble"
    )
    precio_mensual = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Precio mensual"
    )

    # Campos para Direccion
    ubicacion = forms.CharField(max_length=200, label="Dirección")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), label="Comuna")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), label="Region")

    # Campos para Caracteristicas
    m2_construidos = forms.FloatField(label="M² construidos")
    m2_totales = forms.FloatField(label="M² totales")
    estacionamientos = forms.IntegerField(label="Número de estacionamientos")
    habitaciones = forms.IntegerField(label="Número de habitaciones")
    banos = forms.IntegerField(label="Número de baños")

    class Meta:
        model = Inmueble
        fields = [
            "nombre",
            "descripcion",
            "tipo_inmueble",
            "precio_mensual",
            "ubicacion",
            "comuna",
            "m2_construidos",
            "m2_totales",
            "estacionamientos",
            "habitaciones",
            "banos",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Cargar los valores de dirección y características
            self.fields["ubicacion"].initial = self.instance.direccion.ubicacion
            self.fields["comuna"].initial = self.instance.direccion.comuna
            self.fields["m2_construidos"].initial = (
                self.instance.caracteristicas.m2_construidos
            )
            self.fields["m2_totales"].initial = self.instance.caracteristicas.m2_totales
            self.fields["estacionamientos"].initial = (
                self.instance.caracteristicas.estacionamientos
            )
            self.fields["habitaciones"].initial = (
                self.instance.caracteristicas.habitaciones
            )
            self.fields["banos"].initial = self.instance.caracteristicas.banos

    def save(self, commit=True, user=None):
        inmueble = super().save(commit=False)
        if user:
            inmueble.propietario = user

        if commit:
            direccion = Direccion.objects.create(
                ubicacion=self.cleaned_data["ubicacion"],
                comuna=self.cleaned_data["comuna"],
                region=self.cleaned_data["region"],
            )
            direccion.ubicacion = self.cleaned_data["ubicacion"]
            direccion.comuna = self.cleaned_data["comuna"]
            direccion.save()

            # Actualizar las características existentes
            caracteristicas, created = Caracteristicas.objects.get_or_create(
                inmueble=inmueble,
                defaults={
                    "m2_construidos": self.cleaned_data["m2_construidos"],
                    "m2_totales": self.cleaned_data["m2_totales"],
                    "estacionamientos": self.cleaned_data["estacionamientos"],
                    "habitaciones": self.cleaned_data["habitaciones"],
                    "banos": self.cleaned_data["banos"],
                },
            )
            caracteristicas.m2_construidos = self.cleaned_data["m2_construidos"]
            caracteristicas.m2_totales = self.cleaned_data["m2_totales"]
            caracteristicas.estacionamientos = self.cleaned_data["estacionamientos"]
            caracteristicas.habitaciones = self.cleaned_data["habitaciones"]
            caracteristicas.banos = self.cleaned_data["banos"]
            caracteristicas.save()

            inmueble.direccion = direccion
            inmueble.caracteristicas = caracteristicas
            inmueble.save()

        return inmueble


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["fecha_inicio", "fecha_fin"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }
