from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)
    ubicacion = models.CharField(max_length=100, blank=True, default="")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")

    def __str__(self):
        return self.nombre

class MovimientoInventario(models.Model):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    TIPO_CHOICES = [(ENTRADA, 'Entrada'), (SALIDA, 'Salida')]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class OrdenCompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
