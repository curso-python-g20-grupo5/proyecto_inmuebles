# Generated by Django 5.1.3 on 2024-11-24 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inmuebles', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('arrendador', 'Arrendador'), ('arrendatario', 'Arrendatario')], default='arrendatario', max_length=20),
        ),
    ]
