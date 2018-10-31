from django.shortcuts import render,redirect

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
	respaldo = configuracionBDA.objects.get(id = 1)
	if respaldo.respaldo == 1:
		respaldo.respaldo = 0
	else:
		respaldo.respaldo = 1
	respaldo.save()
	return redirect('/gestion/home')
