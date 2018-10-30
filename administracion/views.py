from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from smc.views import logeado
from administracion.models import *

# Create your views here.

@user_passes_test(logeado, login_url = '/login/')
def home(request):
	respaldo = configuracionBDA.objects.get(id = 1)
	return render(request, "administracion/home.html",{'respaldo' : respaldo})

@user_passes_test(logeado, login_url = '/login/')
def configurarRespaldo(request):
	if request.METHOD == 'POST':
		configuracion = configuracionBDA.objects.get(id = 1)
		configuracion.respaldo = request.respaldo
		configuracion.save()

	return render(request, "administracion/home.html")
