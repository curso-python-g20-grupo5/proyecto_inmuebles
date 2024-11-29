#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate


# Load fixtures in the correct order
python manage.py loaddata gestion_inmuebles/fixtures/regiones.json
python manage.py loaddata gestion_inmuebles/fixtures/comunas.json
python manage.py loaddata gestion_inmuebles/fixtures/tipos_inmueble.json
python manage.py loaddata gestion_inmuebles/fixtures/usuarios_perfiles.json
python manage.py loaddata gestion_inmuebles/fixtures/inmuebles.jsonjson

