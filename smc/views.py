from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import login, logout

from causas.models import Causa, Actividad
from personas.models import Persona
from administracion.models import configuracionBDA

def logeado(user):
    return user.is_authenticated

def is_audit(user):
    return user.is_audit

def login_(request):
	return login(request)

def logout_(request):
    return logout(request, next_page=login_)

@user_passes_test(logeado, login_url='/login/')
def index(request):
    return redirect('/home/')

@user_passes_test(logeado, login_url='/login/')
def home(request):
    if request.user.is_audit:
        return render(request, 'auditor/home.html')
    return render(request, 'causas/home.html')

@user_passes_test(logeado, login_url='/login/')
def estadisticas(request):
    causas_pendientes = Causa.objects.filter(
        estado=Causa.PENDIENTE).count()
    causas_atendidas = Causa.objects.exclude(
        estado=Causa.PENDIENTE).count()

    procedencias = []

    for opcion in Causa.OPCIONES_PROCEDENCIA:
        procedencia = {}
        procedencia['tipo'] = opcion[0]
        procedencia['cantidad'] = Causa.objects.filter(
            procedencia=opcion[0]).count
        procedencias.append(procedencia)

    solicitudes = []

    for opcion in Causa.OPCIONES_SOLICITUDES:
        solicitud = {}
        solicitud['tipo'] = opcion[0]
        solicitud['cantidad'] = Causa.objects.filter(
            solicitud=opcion[0]).count()
        solicitudes.append(solicitud)

    delitos = []

    for opcion in Causa.OPCIONES_DELITO:
        delito = {}
        delito['tipo'] = opcion[0]
        delito['cantidad'] = Causa.objects.filter(
            delito=opcion[0]).count()
        delitos.append(delito)

    actividades = []

    for opcion in Actividad.OPCIONES_ACTIVIDAD:
        actividad = {}
        actividad['tipo'] = opcion[0]
        actividad['cantidad'] = Actividad.objects.filter(
            descripcion=opcion[0]).count()
        actividades.append(actividad)

    imputados = Persona.objects.filter(
        condicion=Persona.IMPUTADO).count()

    victimas = Persona.objects.filter(
        condicion=Persona.VICTIMA).count()

    return render(request, 'estadisticas/resultado.html',
        {
            'causas_atendidas': causas_atendidas,
            'causas_pendientes': causas_pendientes,
            'procedencias': procedencias,
            'solicitudes': solicitudes,
            'delitos': delitos,
            'actividades': actividades,
            'imputados': imputados,
            'victimas': victimas,
        })

# def comprobacionRespaldo(request):
    # comp = configuracionBDA.objects.get(id = 1)
    # comp.fecha =