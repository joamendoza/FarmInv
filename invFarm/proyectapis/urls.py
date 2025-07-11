"""
URL configuration for proyectapis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from inventario.views import login_usuario

def redirect_to_store(request):
    return redirect('lista_productos')

urlpatterns = [
    path('', redirect_to_store, name='home'),  # Redirige la URL raíz a la tienda
    path('admin/', admin.site.urls),
    path('inventario/', include('inventario.urls')),
    path('producto/', include('carrito.urls')),
    path('logout/', LogoutView.as_view(next_page='lista_productos'), name='logout'),
    path('inventario/login/', login_usuario, name='login_usuario')
]
