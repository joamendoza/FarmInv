# Generated manually to populate initial data

from django.db import migrations


def populate_initial_data(apps, schema_editor):
    Categoria = apps.get_model('inventario', 'Categoria')
    Proveedor = apps.get_model('inventario', 'Proveedor')
    
    # Crear categorías iniciales si no existen
    categorias_iniciales = [
        'Analgésicos',
        'Antibióticos',
        'Antihistamínicos',
        'Vitaminas y Suplementos',
        'Medicamentos Cardiovasculares',
        'Medicamentos Digestivos',
        'Medicamentos Respiratorios',
        'Productos de Higiene',
        'Primeros Auxilios',
        'Cuidado Personal',
        'Medicamentos Genéricos',
        'Productos Naturales'
    ]
    
    for nombre_categoria in categorias_iniciales:
        categoria, created = Categoria.objects.get_or_create(
            nombre=nombre_categoria
        )
        if created:
            print(f'✅ Categoría creada: {nombre_categoria}')
    
    # Crear proveedores iniciales si no existen
    proveedores_iniciales = [
        {
            'nombre': 'Laboratorios Chile S.A.',
            'contacto': 'Ana García',
            'telefono': '+56 2 2345 6789',
            'email': 'contacto@labchile.cl'
        },
        {
            'nombre': 'FarmaCorp Internacional',
            'contacto': 'Carlos Mendoza',
            'telefono': '+56 9 8765 4321',
            'email': 'ventas@farmacorp.cl'
        },
        {
            'nombre': 'Distribuidora MedSupply',
            'contacto': 'María López',
            'telefono': '+56 2 3456 7890',
            'email': 'pedidos@medsupply.cl'
        },
        {
            'nombre': 'Laboratorio Nacional',
            'contacto': 'José Rodríguez',
            'telefono': '+56 9 1234 5678',
            'email': 'info@labnacional.cl'
        },
        {
            'nombre': 'PharmaTech Solutions',
            'contacto': 'Patricia Silva',
            'telefono': '+56 2 4567 8901',
            'email': 'contacto@pharmatech.cl'
        }
    ]
    
    for proveedor_data in proveedores_iniciales:
        proveedor, created = Proveedor.objects.get_or_create(
            nombre=proveedor_data['nombre'],
            defaults={
                'contacto': proveedor_data['contacto'],
                'telefono': proveedor_data['telefono'],
                'email': proveedor_data['email']
            }
        )
        if created:
            print(f'✅ Proveedor creado: {proveedor_data["nombre"]}')


def reverse_populate_initial_data(apps, schema_editor):
    # No necesitamos hacer nada en el reverse, ya que son datos iniciales
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_producto_fecha_vencimiento_producto_proveedor'),
    ]

    operations = [
        migrations.RunPython(
            populate_initial_data,
            reverse_populate_initial_data
        ),
    ]
