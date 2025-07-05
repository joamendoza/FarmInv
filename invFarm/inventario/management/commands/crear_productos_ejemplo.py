from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from inventario.models import Producto, Categoria, Proveedor
import random


class Command(BaseCommand):
    help = 'Crea productos de ejemplo para el sistema de inventario'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Número de productos a crear (por defecto: 20)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Verificar que existen categorías y proveedores
        if not Categoria.objects.exists():
            self.stdout.write(
                self.style.ERROR('No hay categorías. Ejecuta las migraciones primero.')
            )
            return
            
        if not Proveedor.objects.exists():
            self.stdout.write(
                self.style.ERROR('No hay proveedores. Ejecuta las migraciones primero.')
            )
            return

        categorias = list(Categoria.objects.all())
        proveedores = list(Proveedor.objects.all())

        # Productos de ejemplo para farmacia
        productos_ejemplo = [
            {'nombre': 'Paracetamol 500mg', 'precio': 2500, 'categoria': 'Analgésicos'},
            {'nombre': 'Ibuprofeno 400mg', 'precio': 3200, 'categoria': 'Analgésicos'},
            {'nombre': 'Aspirina 100mg', 'precio': 1800, 'categoria': 'Analgésicos'},
            {'nombre': 'Amoxicilina 500mg', 'precio': 8500, 'categoria': 'Antibióticos'},
            {'nombre': 'Azitromicina 250mg', 'precio': 12000, 'categoria': 'Antibióticos'},
            {'nombre': 'Loratadina 10mg', 'precio': 4500, 'categoria': 'Antihistamínicos'},
            {'nombre': 'Cetirizina 10mg', 'precio': 3800, 'categoria': 'Antihistamínicos'},
            {'nombre': 'Vitamina C 1000mg', 'precio': 6500, 'categoria': 'Vitaminas y Suplementos'},
            {'nombre': 'Complejo B', 'precio': 9200, 'categoria': 'Vitaminas y Suplementos'},
            {'nombre': 'Vitamina D3 2000UI', 'precio': 11500, 'categoria': 'Vitaminas y Suplementos'},
            {'nombre': 'Enalapril 10mg', 'precio': 7800, 'categoria': 'Medicamentos Cardiovasculares'},
            {'nombre': 'Losartán 50mg', 'precio': 9500, 'categoria': 'Medicamentos Cardiovasculares'},
            {'nombre': 'Omeprazol 20mg', 'precio': 5600, 'categoria': 'Medicamentos Digestivos'},
            {'nombre': 'Ranitidina 150mg', 'precio': 4200, 'categoria': 'Medicamentos Digestivos'},
            {'nombre': 'Salbutamol Inhalador', 'precio': 15800, 'categoria': 'Medicamentos Respiratorios'},
            {'nombre': 'Alcohol Gel 70%', 'precio': 2200, 'categoria': 'Productos de Higiene'},
            {'nombre': 'Mascarillas Quirúrgicas', 'precio': 8900, 'categoria': 'Productos de Higiene'},
            {'nombre': 'Vendas Elásticas', 'precio': 3500, 'categoria': 'Primeros Auxilios'},
            {'nombre': 'Gasa Estéril', 'precio': 1800, 'categoria': 'Primeros Auxilios'},
            {'nombre': 'Termómetro Digital', 'precio': 12500, 'categoria': 'Cuidado Personal'},
            {'nombre': 'Glucómetro + Tiras', 'precio': 28000, 'categoria': 'Cuidado Personal'},
            {'nombre': 'Jarabe para la Tos', 'precio': 6800, 'categoria': 'Medicamentos Respiratorios'},
            {'nombre': 'Crema Hidratante', 'precio': 4500, 'categoria': 'Cuidado Personal'},
            {'nombre': 'Protector Solar FPS 50', 'precio': 18500, 'categoria': 'Cuidado Personal'},
            {'nombre': 'Suero Fisiológico', 'precio': 2800, 'categoria': 'Primeros Auxilios'},
        ]

        productos_creados = 0
        
        for i in range(min(count, len(productos_ejemplo))):
            producto_data = productos_ejemplo[i]
            
            # Buscar la categoría correspondiente
            categoria = None
            for cat in categorias:
                if cat.nombre == producto_data['categoria']:
                    categoria = cat
                    break
            
            if not categoria:
                categoria = random.choice(categorias)

            # Generar fecha de vencimiento aleatoria (6 meses a 3 años)
            dias_vencimiento = random.randint(180, 1095)
            fecha_vencimiento = timezone.now().date() + timedelta(days=dias_vencimiento)

            # Stock aleatorio
            stock = random.randint(5, 200)

            # Crear el producto
            producto, created = Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults={
                    'descripcion': f'Medicamento/producto farmacéutico {producto_data["nombre"]}',
                    'precio': producto_data['precio'],
                    'stock': stock,
                    'categoria': categoria,
                    'proveedor': random.choice(proveedores),
                    'fecha_vencimiento': fecha_vencimiento
                }
            )

            if created:
                productos_creados += 1
                self.stdout.write(
                    f'✅ Producto creado: {producto.nombre} - Stock: {producto.stock} - Precio: ${producto.precio}'
                )
            else:
                self.stdout.write(
                    f'⚠️  Producto ya existe: {producto.nombre}'
                )

        # Si necesitamos más productos, crear algunos genéricos
        if count > len(productos_ejemplo):
            productos_restantes = count - len(productos_ejemplo)
            
            for i in range(productos_restantes):
                nombre = f'Medicamento Genérico {i+1}'
                
                producto, created = Producto.objects.get_or_create(
                    nombre=nombre,
                    defaults={
                        'descripcion': f'Producto farmacéutico genérico número {i+1}',
                        'precio': random.randint(1500, 25000),
                        'stock': random.randint(5, 150),
                        'categoria': random.choice(categorias),
                        'proveedor': random.choice(proveedores),
                        'fecha_vencimiento': timezone.now().date() + timedelta(days=random.randint(180, 1095))
                    }
                )

                if created:
                    productos_creados += 1
                    self.stdout.write(
                        f'✅ Producto genérico creado: {producto.nombre} - Stock: {producto.stock}'
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Proceso completado! Se crearon {productos_creados} productos nuevos.'
            )
        )
        
        # Mostrar estadísticas
        total_productos = Producto.objects.count()
        total_stock = sum(p.stock for p in Producto.objects.all())
        
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 Estadísticas del inventario:\n'
                f'   • Total de productos: {total_productos}\n'
                f'   • Stock total: {total_stock} unidades\n'
                f'   • Categorías disponibles: {Categoria.objects.count()}\n'
                f'   • Proveedores registrados: {Proveedor.objects.count()}'
            )
        )
