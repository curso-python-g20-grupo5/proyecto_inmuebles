# Proyecto: Sistema de Gestión de Inmuebles

Este proyecto es una aplicación web desarrollada con **Django** que permite a usuarios revisar, gestionar y administrar inmuebles disponibles para arriendo. La aplicación utiliza el patrón **MVC** y está diseñada para cubrir funcionalidades tanto para arrendatarios como para arrendadores.

## Requisitos del Sistema

- **Python 3.9+**
- **Django 5.1.3**
- **PostgreSQL**

- **Dependencias necesarias:**

   ```bash
   Django
   psycopg2-binary (para conectar Django con PostgreSQL)
   ```

- **Dependencias adicionales:**

  ```bash
  asgiref==3.8.1
  pillow==11.0.0
  psycopg2==2.9.10
  python-dotenv==1.0.1
  sqlparse==0.5.2
  typing_extensions==4.12.2
  tzdata==2024.2
  ```

## Configuración Inicial

1. **Clonar el repositorio:**

   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. **Crear y activar un entorno virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate # En Windows: venv\Scripts\activate
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**

   Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=<nombre_base_datos>
   DB_USER=<usuario>
   DB_PASSWORD=<contraseña>
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Aplicar migraciones y ejecutar fixtures para carga inicial de data:**

   ```bash
   python manage.py migrate
   python manage.py loaddata fixtures/regiones.json
   python manage.py loaddata fixtures/comunas.json
   python manage.py loaddata fixtures/tipos_inmueble.json
   python manage.py loaddata fixtures/usuarios_perfiles.json
   python manage.py loaddata fixtures/inmuebles.json
   ```

    > [!TIP]
    > Contraseña para los usuarios cargados: 123Pass4

6. **Iniciar el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

## Características

- **Base de Datos Relacional:**
  - Modelado de datos utilizando los conceptos de claves primarias y foráneas.
  - Conexión y manejo de datos en PostgreSQL.
- **Operaciones CRUD:**
  - Crear: Inserción de nuevos inmuebles.
  - Leer: Listado de inmuebles disponibles.
  - Actualizar: Modificación de registros existentes.
  - Borrar: Eliminación de registros desde los modelos.
- **Configuración documentada:**
  - Todo el proceso de instalación, desarrollo y pruebas está documentado para facilitar la reproducción del entorno.

### Abre la shell de Django

```cmd
python manage.py shell
```

### Importa el modelo TipoInmueble

```cmd
from gestion_inmuebles.models import TipoInmueble
```

### Crea instancias de TipoInmueble y guárdalas en la base de datos

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

### Verifica que los tipos de inmuebles se hayan creado correctamente

```cmd
# Consultar todos los tipos de inmuebles
tipos = TipoInmueble.objects.all()
for tipo in tipos:
    print(tipo)
```

### Encuentra el registro que deseas actualizar y realiza el cambio

```cmd
# Encuentra el tipo de inmueble "Apartamento"
tipo_apartamento = TipoInmueble.objects.get(tipo="Apartamento")

# Edita el tipo a "Departamento"
tipo_apartamento.tipo = "Departamento"
tipo_apartamento.save()
```

### Verifica que el cambio se haya realizado correctamente

```cmd
# Consultar todos los tipos de inmuebles para verificar el cambio
tipos = TipoInmueble.objects.all()
for tipo in tipos:
    print(tipo)
```

## Estructura del Proyecto

- **`proyecto_inmuebles/`**: Configuración principal del proyecto.
- **`gestion_inmuebles/`**: Aplicación para la gestión de usuarios, inmuebles y reservas.
- **`templates/`**: Contiene los archivos HTML.
- **`fixtures/`**: Archivos JSON para poblar la base de datos.
- **`static/`**: Archivos CSS, JS e imágenes.

## Funcionalidades del Proyecto

### Hito 4.1: Administración de Usuarios

1. **Login de Usuarios:**
   - URL: `/login/`
   - Permite a los usuarios autenticarse en el sistema.
   - Implementación en `views.py` usando `AuthenticationForm`.

2. **Registro de Usuarios:**
   - URL: `/register/`
   - Utiliza un formulario personalizado (`CustomUserCreationForm`).

3. **Página Personal de Perfil:**
   - URL: `/accounts/profile/`
   - Los usuarios pueden ver y editar sus datos personales.

4. **Modificación de Datos Personales:**
   - Permite actualizar el nombre, apellido, correo y tipo de usuario (Arrendador o Arrendatario).
   - Implementación en `UserProfileForm` y vista `profile_view`.

### Hito 4.2: Gestión de Inmuebles y Datos Geográficos

1. **Agregar Nuevos Inmuebles:**
   - URL: `/crear-propiedad/`
   - Permite a los arrendadores agregar nuevas propiedades.
   - Incluye un formulario (`InmuebleForm`) que combina datos de dirección, características y tipo de inmueble.

2. **Actualizar/Borrar Inmuebles:**
   - URL para actualizar: `/editar-propiedad/<int:propiedad_id>/`
   - URL para eliminar: `/eliminar-propiedad/<int:propiedad_id>/`
   - Los arrendadores pueden modificar o eliminar propiedades existentes.

3. **Listar Propiedades Disponibles:**
   - URL: `/search/`
   - Vista de búsqueda para que arrendatarios revisen inmuebles.
   - Filtros disponibles: región, comuna, tipo de inmueble, rango de precios.

4. **Datos Geográficos:**
   - La base de datos incluye información sobre regiones y comunas de Chile.
   - Datos precargados desde los archivos `regiones.json` y `comunas.json`.

5. **Reservas:**
   - Los arrendatarios pueden realizar, ver y cancelar reservas.
   - Implementación en las vistas `mis_reservas` y `cancelar_reserva`.

## Scripts para Datos

1. **Scripts JSON:**
   - `regiones.json`: Contiene las regiones de Chile.
   - `comunas.json`: Contiene las comunas de cada región.
   - `tipos_inmueble.json`: Define tipos de inmuebles.
   - `usuarios_perfiles.json`: Usuarios de prueba con sus perfiles.
   - `inmuebles.json`: Inmuebles de prueba.

## Hito 2 parte 1

Archivo de evidencia Hito 2: [https://docs.google.com/document/d/1ZMJwCxJuNW4HzT5UYEdHY5rOSdP8s5wRNl85uTGgCdM/edit?tab=t.0]

## Hito 2 parte 2

Archivo de evidencia Hito 2:[https://docs.google.com/document/d/1ZMJwCxJuNW4HzT5UYEdHY5rOSdP8s5wRNl85uTGgCdM/edit?tab=t.3aku1dava30x]

## Instrucciones para Contribuir

1. Realiza un fork del repositorio.
2. Crea una rama para tu funcionalidad o corrección:

   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

3. Haz commits claros y descriptivos.
4. Abre un Pull Request explicando los cambios realizados.

## Autores y Autoras

- [Rosa Rubio](https://github.com/PaulinaRubioP)
- [Valery Maragaño](https://github.com/Valyxp)
- [Marco Alvarado](https://github.com/7pixel-cl)
- [Esteban Hernández](https://github.com/stivhc)

  ```bash
  ⌨️ con ❤️ por el Grupo 3 - G20 😊
  ```
