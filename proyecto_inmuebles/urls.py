"""
URL configuration for proyecto_inmuebles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from gestion_inmuebles import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.landing_view, name="landing"),
    path("login/", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("", views.home, name="home"),
    path("accounts/profile/", views.profile_view, name="profile"),
    path("search/", views.search_properties, name="search_properties"),
    path("property/<int:pk>/", views.property_detail, name="property_detail"),
    path("api/comunas/", views.get_comunas, name="get_comunas"),
    path(
        "editar-propiedad/<int:propiedad_id>/",
        views.editar_propiedad,
        name="editar_propiedad",
    ),
    path("mis-reservas/", views.mis_reservas, name="mis_reservas"),
    path(
        "cancelar-reserva/<int:reserva_id>/",
        views.cancelar_reserva,
        name="cancelar_reserva",
    ),
    path("crear-propiedad/", views.crear_propiedad, name="crear_propiedad"),
    path(
        "eliminar-propiedad/<int:propiedad_id>/",
        views.eliminar_propiedad,
        name="eliminar_propiedad",
    ),
    path(
        "aceptar-arrendatario/<int:reserva_id>/",
        views.aceptar_arrendatario,
        name="aceptar_arrendatario",
    ),
    path("mis-propiedades/", views.mis_propiedades, name="mis_propiedades"),
]
