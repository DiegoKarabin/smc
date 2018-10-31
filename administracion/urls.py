from django.urls import path

from . import views

app_name = 'apps'

urlpatterns = [
	path('home/', views.home),
	path('respaldo/', views.configurarRespaldo, name = 'respaldo'),
]