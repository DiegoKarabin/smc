from django.urls import path

from . import views

app_name = 'apps'

urlpatterns = [
	path('home/', views.home, name = 'home'),
	path('respaldo/', views.configurarRespaldo, name = 'respaldo'),
	path('exportar/',views.crearRespaldo, name = 'exportar'),
	path('change/',views.cambiarPeriodo, name = 'change'),
	path('han_pasado/', views.respaldosAutomaticos, name = 'han_pasado')
]