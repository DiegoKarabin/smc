from django.urls import path

from . import views

urlpatterns = [
    path('', views.ver_causas),
    path('buscar/', views.buscar),
    path('ver/<nro_expediente>/', views.ver_causa),
    path('modificar/<nro_expediente>/', views.modificar_causa),
    path('eliminar/<nro_expediente>/', views.eliminar_causa),
    path('ingreso/', views.nueva_causa),
    path('remover/<int:ci>/de/<nro_expediente>', views.remover_persona),
    path('actividades/nueva/', views.agregar_actividad),
    path('actividades/registrar', views.registrar_actividad),
    path('triaje/<nro_expediente>/', views.agregar_triaje),
]
