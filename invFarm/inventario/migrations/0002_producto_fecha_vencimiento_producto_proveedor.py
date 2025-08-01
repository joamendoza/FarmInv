# Generated by Django 5.2.1 on 2025-07-05 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='fecha_vencimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Vencimiento'),
        ),
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.proveedor', verbose_name='Proveedor'),
        ),
    ]
