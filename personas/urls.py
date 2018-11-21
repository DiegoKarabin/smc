from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar),
    path('agregar-a-<nro_expediente>/', views.agregar_persona),
    path('<int:ci>/', views.ver_persona),
    path('victimas/', views.ver_victimas),
    path('imputados/', views.ver_imputados),
    path('modificar/<int:ci>/', views.modificar_persona),
    path('eliminar/<int:ci>/', views.eliminar_persona),
    path('remover/<int:id>/de/<int:ci>', views.remover_actividad),
    path('fallas', views.procesar_falla),
]
