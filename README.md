# Proyecto Inmuebles
Este proyecto es un sitio web desarrollado con Django, diseñado para gestionar y visualizar viviendas disponibles para arriendo. Es parte de un desafío evaluado que conecta Django a una base de datos PostgreSQL, permitiendo realizar operaciones CRUD y definiendo relaciones entre los datos.

## Entorno de desarrollo

1. PostgreSQL: Instalación y configuración del servidor de base de datos.
2. Entorno virtual de Python: Creación y activación.
3. Dependencias necesarias:
       - Django
       - psycopg2-binary (para conectar Django con PostgreSQL)
4. Aplicación Django: Configuración inicial del proyecto y sus aplicaciones.

## Características

* Base de Datos Relacional:
  - Modelado de datos utilizando los conceptos de claves primarias y foráneas.
  - Conexión y manejo de datos en PostgreSQL.
* Operaciones CRUD:
  - Crear: Inserción de nuevos inmuebles.
  - Leer: Listado de inmuebles disponibles.
  - Actualizar: Modificación de registros existentes.
  - Borrar: Eliminación de registros desde los modelos.
* Configuración documentada:
  - Todo el proceso de instalación, desarrollo y pruebas está documentado para facilitar la reproducción del entorno.

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
