from django.urls import path

from . import views

app_name = 'apps'

urlpatterns = [
	path('home/', views.home, name = 'home'),
	path('respaldo/', views.configurarRespaldo, name = 'respaldo'),
	path('table/',views.crearRespaldo, name = 'table'),
	path('change/',views.cambiarPeriodo, name = 'change'),
	path('bitacora/', views.ver_bitacora, name = 'bitacora'),
	path('bitacora_transacciones/', views.ver_bitacora_transacciones, name='bitacora_transacciones'),
]