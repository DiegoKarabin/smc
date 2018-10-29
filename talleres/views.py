from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from datetime import date, timedelta

from .models import Grupo, Sesion
from .forms import FormularioTaller
from causas.models import Persona
from causas.views import logeado

# Create your views here.
@user_passes_test(logeado, login_url='/login/')
def crear_taller(request):
	formulario = FormularioTaller()

	if request.method == 'POST':
		formulario = FormularioTaller(request.POST)

		if formulario.is_valid():
			datos = formulario.cleaned_data

			try:
				g = Grupo.objects.get(nombre=datos['nombre'])
				formulario.add_error(None,
					{'nombre': 'Ya existe un grupo registrado con ese nombre'})
				return render(request, 'talleres/formulario_taller.html',
							  {'formulario': formulario})
			except:
				nombre = datos['nombre']
				tematica = datos['tematica']
				inicio = datos['fecha_inicio']
				cant_sesiones = datos['sesiones']
				final = inicio + timedelta(days=(cant_sesiones - 1) * 28)

				grupo = Grupo.objects.create(
					nombre=nombre,
					tematica=tematica,
					fecha_inicio=inicio,
					fecha_final=final
				)

				for x in range(cant_sesiones):
					Sesion.objects.create(
						fecha=inicio + timedelta(days=(x * 28)),
						estado=Sesion.PENDIENTE,
						grupo=grupo
					)

				return redirect('/talleres/')
	return render(request, 'talleres/formulario_taller.html', {'formulario': formulario})

@user_passes_test(logeado, login_url='/login/')
def ver_talleres(request):
	grupos_talleres = Grupo.objects.all()
	return render(request, 'talleres/talleres.html',
		{
			'grupos':grupos_talleres
		})

@user_passes_test(logeado, login_url='/login/')
def ver_taller(request, nombre):
	if nombre == 'agregar_a_taller':
		return agregar_a_taller(request)
		
	try:
		grupo = Grupo.objects.get(nombre=nombre)
	except:
		return render(request, 'talleres/no_existe.html')

	return render(request, 'talleres/info_taller.html',
		{
			'grupo':grupo
		})

@user_passes_test(logeado, login_url='/login')
def buscar(request):
	q = request.GET.get('nombre', '')

	if q:
		return redirect('/talleres/' + q + '/')
	else:
		return redirect('/talleres/')

@user_passes_test(logeado, login_url='/login/')
def agregar_a_taller(request):
	if request.method == 'POST' and all(request.POST.values()):
		ci = request.POST.get('ci', '')
		lista_talleres = Grupo.objects.all()
		return render(request, 'talleres/talleres.html',
			{
				'grupos':lista_talleres,
				'agregar':True,
				'ci':ci
			})
	return redirect('/causas/')

@user_passes_test(logeado, login_url='/login/')
def agregar_persona(request, nombre, ci):
	grupo = Grupo.objects.get(nombre=nombre)
	persona = Persona.objects.get(ci=ci)

	if grupo and persona:
		if len(grupo.participantes.get_queryset()) == 0:
			grupo.participantes.set((persona,))
		else:
			grupo.participantes.add(persona)
		return redirect('/talleres/' + nombre + '/')
	return redirect('/causas/')
