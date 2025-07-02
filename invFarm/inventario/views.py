from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto, MovimientoInventario, Proveedor, OrdenCompra, Proyecto
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductoSerializer
from functools import wraps

class ProductoListView(ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'

    def get_queryset(self):
        return Producto.objects.all()  # Mostrar todos los productos

class ProductoCreateView(CreateView):
    model = Producto
    fields = ['nombre', 'categoria', 'descripcion', 'precio', 'stock', 'ubicacion']
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'categoria', 'descripcion', 'precio', 'stock', 'ubicacion']
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return redirect(self.success_url)

class ProductoListAPIView(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductoDetailAPIView(APIView):
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

# Vistas protegidas según grupo

@login_required
def producto_list(request):
    productos = Producto.objects.all()  # Mostrar todos los productos
    return render(request, 'inventario/producto_list.html', {'productos': productos})

@login_required
def producto_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        ubicacion = request.POST.get("ubicacion")
        Producto.objects.create(
            nombre=nombre,
            categoria=categoria,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            ubicacion=ubicacion,
            activo=True
        )
        return redirect('producto_list')
    return render(request, 'inventario/producto_form.html')

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.categoria = request.POST.get("categoria")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")
        producto.ubicacion = request.POST.get("ubicacion")
        producto.save()
        return redirect('producto_list')
    return render(request, 'inventario/producto_form.html', {'producto': producto})

@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.activo = False
        producto.save()
        return redirect('producto_list')
    return render(request, 'inventario/producto_confirm_delete.html', {'producto': producto})

@login_required
def registrar_entrada(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad"))
        MovimientoInventario.objects.create(
            producto=producto,
            tipo='entrada',
            cantidad=cantidad,
            usuario=request.user
        )
        producto.stock += cantidad
        producto.save()
        return redirect('producto_list')
    return render(request, 'inventario/registrar_entrada.html', {'producto': producto})

@login_required
def registrar_salida(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad"))
        if cantidad > producto.stock:
            return render(request, 'inventario/registrar_salida.html', {'producto': producto, 'error': 'No hay suficiente stock.'})
        MovimientoInventario.objects.create(
            producto=producto,
            tipo='salida',
            cantidad=cantidad,
            usuario=request.user
        )
        producto.stock -= cantidad
        producto.save()
        return redirect('producto_list')
    return render(request, 'inventario/registrar_salida.html', {'producto': producto})

@login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'inventario/lista_proveedores.html', {'proveedores': proveedores})

@login_required
def crear_proveedor(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        contacto = request.POST.get("contacto")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        Proveedor.objects.create(nombre=nombre, contacto=contacto, telefono=telefono, email=email)
        return redirect('lista_proveedores')
    return render(request, 'inventario/crear_proveedor.html')

@login_required
def lista_ordenes_compra(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'inventario/lista_ordenes_compra.html', {'ordenes': ordenes})

@login_required
def crear_orden_compra(request):
    proveedores = Proveedor.objects.all()
    if request.method == "POST":
        proveedor_id = request.POST.get("proveedor")
        proveedor = Proveedor.objects.get(id=proveedor_id)
        OrdenCompra.objects.create(proveedor=proveedor, usuario=request.user)
        return redirect('lista_ordenes_compra')
    return render(request, 'inventario/crear_orden_compra.html', {'proveedores': proveedores})

@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'inventario/lista_proyectos.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            responsable=request.user
        )
        return redirect('lista_proyectos')
    return render(request, 'inventario/crear_proyecto.html')

@login_required
def reporte_inventario(request):
    productos = Producto.objects.all()
    movimientos = MovimientoInventario.objects.all().order_by('-fecha')
    return render(request, 'inventario/reporte_inventario.html', {'productos': productos, 'movimientos': movimientos})

@login_required
def panel_gestion_inventario(request):
    return render(request, 'inventario/panel_gestion_inventario.html')

# Las vistas de registro y login quedan públicas
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_productos')
    else:
        form = UserCreationForm()
    return render(request, 'inventario/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lista_productos')
    else:
        form = AuthenticationForm()
    return render(request, 'inventario/login.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test

def usuario_con_grupo_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.groups.exists())(view_func)
