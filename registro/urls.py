from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

 	path('usuarios/crear', views.crearUsuario, name='usuario-crear'),

    path('clientes/', views.cliente_list_view, name='cliente-lista'),
    path('clientes/crear', views.cliente_create_view, name='cliente-crear'),
    path('clientes/<int:id>', views.cliente_detail_view, name='cliente-detalle'),

    path('tipos/', views.tipo_list_view, name='tipo-lista'),
    path('tipos/crear', views.tipo_create_view, name='tipo-crear'),

    path('trabajos/crear', views.trabajo_create_view, name='trabajo-crear'),
]
