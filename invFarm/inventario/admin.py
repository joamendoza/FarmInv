from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'stock', 'precio', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo', 'categoria')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
