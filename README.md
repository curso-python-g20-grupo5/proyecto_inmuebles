## Proyecto Inmuebles

### Abre la shell de Django:

```cmd
python manage.py shell
```

### Importa el modelo TipoInmueble:

```cmd
from gestion_inmuebles.models import TipoInmueble
```

### Crea instancias de TipoInmueble y guárdalas en la base de datos:

```cmd
# Crear tipos de inmuebles
tipo1 = TipoInmueble(tipo="Apartamento")
tipo1.save()

tipo2 = TipoInmueble(tipo="Casa")
tipo2.save()

tipo3 = TipoInmueble(tipo="Oficina")
tipo3.save()

tipo4 = TipoInmueble(tipo="Terreno")
tipo4.save()
```

### Verifica que los tipos de inmuebles se hayan creado correctamente:

```cmd
# Consultar todos los tipos de inmuebles
tipos = TipoInmueble.objects.all()
for tipo in tipos:
    print(tipo)
```

### Encuentra el registro que deseas actualizar y realiza el cambio:

```cmd
# Encuentra el tipo de inmueble "Apartamento"
tipo_apartamento = TipoInmueble.objects.get(tipo="Apartamento")

# Edita el tipo a "Departamento"
tipo_apartamento.tipo = "Departamento"
tipo_apartamento.save()
```

### Verifica que el cambio se haya realizado correctamente:

```cmd
# Consultar todos los tipos de inmuebles para verificar el cambio
tipos = TipoInmueble.objects.all()
for tipo in tipos:
    print(tipo)
```
