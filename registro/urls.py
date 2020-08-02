from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('contadores/', views.contador_list_view, name='contador-lista'),
 	path('contadores/crear/', views.contador_create_view, name='contador-crear'),
    path('contadores/<int:id>/', views.contador_detail_view, name='contador-detalle'),
    path('contadores/<int:id>/editar/', views.contador_update_view, name='contador-editar'),
    
    path('clientes/', views.cliente_list_view, name='cliente-lista'),
    path('clientes/crear', views.cliente_create_view, name='cliente-crear'),
    path('clientes/<int:id>', views.cliente_detail_view, name='cliente-detalle'),
    path('clientes/<int:id>/editar', views.cliente_update_view, name='cliente-editar'),

    path('tipos/', views.tipo_list_view, name='tipo-lista'),
    path('tipos/crear', views.tipo_create_view, name='tipo-crear'),
    path('tipos/<int:id>', views.tipo_detail_view, name='tipo-detalle'),
    path('tipos/<int:id>/editar/', views.tipo_update_view, name='tipo-editar'),

    path('trabajos/', views.trabajo_list_view, name='trabajo-lista'),
    path('trabajos/crear', views.trabajo_create_view, name='trabajo-crear'),
    path('trabajos/<int:id>', views.trabajo_detail_view, name='trabajo-detalle'),
    path('trabajos/<int:id>/editar/', views.trabajo_update_view, name='trabajo-editar'),
    path('trabajos/todos/', views.trabajo_todos_view, name='trabajo-todos'),
    path('trabajos/todos/exportar/', views.trabajo_to_excel, name='trabajo-exportar'),
]
