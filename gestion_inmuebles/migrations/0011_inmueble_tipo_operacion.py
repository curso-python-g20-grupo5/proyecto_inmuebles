# Generated by Django 5.1.3 on 2024-11-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inmuebles', '0010_remove_inmueble_image_filename_inmueble_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='tipo_operacion',
            field=models.CharField(choices=[('venta', 'Venta'), ('arriendo', 'Arriendo')], default='arriendo', max_length=10),
        ),
    ]