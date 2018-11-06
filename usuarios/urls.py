from django.urls import path

from . import views

urlpatterns = [
    path('', views.ver_usuarios),
    path('buscar/', views.buscar),
    path('agregar/', views.agregar_usuario),
    path('ver/<ci>/', views.ver_usuario),
    path('modificar/<ci>/', views.modificar_usuario),
    path('eliminar/<ci>/', views.eliminar_usuario),
    path('inhabilitar/<ci>/', views.inhabilitar_usuario),
    path('cambiar_clave/', views.cambiar_clave),
    path('sin_permiso/', views.sin_permiso),
]
