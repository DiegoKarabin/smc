from django.urls import path
from . import views

urlpatterns = [
	path('', views.ver_talleres, name='ver_talleres'),
	path('buscar/', views.buscar, name='buscar'),
    path('nuevo/', views.crear_taller, name='nuevo_taller'),
    path('<nombre>/', views.ver_taller, name='taller'),
    path('<nombre>/agregar/<int:ci>', views.agregar_persona, name='agregar_persona'),
]
