from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='lista_productos'), name='logout'),
    path('prueba/', lambda request: HttpResponse("¡Funciona!")),  # <-- Añade esto temporalmente
    path('inventario/', include('inventario.urls')),
    path('', include('carrito.urls')),
]