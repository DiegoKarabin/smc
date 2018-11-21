from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

import json

from smc.views import logeado
from causas.models import Causa, Actividad
from usuarios.models import BitacoraAcceso
from administracion.models import BitacoraTransaccion
from .models import Persona
from .forms import FormularioPersona

# Create your views here.


@user_passes_test(logeado, login_url='/login/')
def agregar_persona(request, nro_expediente):
    formulario = FormularioPersona(initial={'ci': '', 'edad': ''})

    if request.method == 'POST':
        formulario = FormularioPersona(request.POST)

        if formulario.is_valid():
            causa = Causa.objects.get(nro_expediente=nro_expediente)
            persona = formulario.cleaned_data
            persona = causa.personas.create(**persona)

            BitacoraAcceso.objects.create(
                usuario=request.user,
                tabla='personas_persona',
                registro=persona.ci,
                accion='Insertar'
            )

            return redirect('/causas/ver/' + nro_expediente + '/')

    return render(request, 'formulario.html',
                  {
                      'titulo': 'Agregar Persona',
                      'formulario': formulario
                  })


@user_passes_test(logeado, login_url='/login/')
def ver_persona(request, ci):
    try:
        persona = Persona.objects.get(ci=ci)

        BitacoraAcceso.objects.create(
            usuario=request.user,
            tabla='personas_persona',
            registro=persona.ci,
            accion='Consultar'
        )
    except:

        return render(request, 'personas/no_existe.html')
    return render(request, 'personas/info.html',
      {
        'persona': persona
      })

@user_passes_test(logeado, login_url='/login/')
def buscar(request):
    q = request.GET.get('ci', '')

    if q:
        if not q.isdigit():
            return render(request, 'personas/no_existe.html')
        else:
            return redirect('/personas/' + q + '/')
    else:
        return redirect('/home')

def registrar_transaccion(persona, datos):
    nro_transaccion = (BitacoraTransaccion.objects
                                          .filter(accion__icontains='Iniciar')
                                          .count()) + 1
    BitacoraTransaccion.objects.create(
        accion='Iniciar <T{}>'.format(nro_transaccion)
    )

    for (clave, valor) in datos.items():
        try:
            viejo = getattr(persona, clave)
            nuevo = valor

            if viejo != nuevo:
                BitacoraTransaccion.objects.create(
                    accion='Leer',
                    tabla='personas_persona',
                    campo=clave,
                    registro=persona.ci
                )
        except AttributeError:
            pass
    
    for (clave, valor) in datos.items():
        try:
            viejo = getattr(persona, clave)
            nuevo = valor

            if viejo != nuevo:
                BitacoraTransaccion.objects.create(
                    accion='Escribir',
                    tabla='personas_persona',
                    campo=clave,
                    registro=persona.ci,
                    valor_anterior=viejo,
                    valor_actual=nuevo
                )

            if 'falla_en' in datos.keys() and datos['falla_en'] == clave:
                return
        except AttributeError:
            pass

    BitacoraTransaccion.objects.create(
        accion='Commit'
    )

@user_passes_test(logeado, login_url='/login/')
def modificar_persona(request, ci):
    persona = Persona.objects.get(ci=ci)

    if not persona.edit:
        persona.edit = True
        persona.is_editing = request.user.ci
        persona.save()
    
    if persona.edit and request.user.ci == persona.is_editing:
        if request.method == 'POST':
            registrar_transaccion(persona, request.POST)

            formulario = FormularioPersona(request.POST, instance=persona)

            if formulario.is_valid():
                persona.edit = False
                persona.save()

                BitacoraAcceso.objects.create(
                    usuario=request.user,
                    tabla='personas_persona',
                    registro=persona.ci,
                    accion='Modificar'
                )

                formulario.save()
                return redirect('/personas/%d/' % ci)

        formulario = FormularioPersona(instance=persona)
        actividades = persona.actividad_set.all()

        return render(request, 'personas/formulario.html',
                    {
                        'formulario': formulario,
                        'titulo': 'Modificar %s %s' % (persona.nombre,
                                                       persona.apellido),
                        'ci': ci,
                        'actividades': actividades,
                    })
    else:
      return redirect('/edit_bloqueado.html')


@user_passes_test(logeado, login_url='/login/')
def eliminar_persona(request, ci):
    persona = Persona.objects.get(ci=ci)
    condicion = persona.condicion

    if persona:
        persona_id = persona.id
        BitacoraAcceso.objects.create(
            usuario=request.user,
            tabla='personas_persona',
            registro=persona.ci,
            accion='Eliminar'
        )
        persona.delete()

    if condicion == Persona.VICTIMA:
        a_donde = 'victimas'
    else:
        a_donde = 'imputados'

    return redirect('/personas/' + a_donde + '/')


@user_passes_test(logeado, login_url='/login/')
def ver_victimas(request):
    victimas = Persona.objects.filter(condicion=Persona.VICTIMA)
    return render(request, 'personas/victimas.html',
      {
        'victimas': victimas
      })


@user_passes_test(logeado, login_url='/login/')
def ver_imputados(request):
    imputados = Persona.objects.filter(condicion=Persona.IMPUTADO)
    return render(request, 'personas/imputados.html',
      {
        'imputados': imputados
      })


@user_passes_test(logeado, login_url='login')
def remover_actividad(request, id, ci):
    actividad = Actividad.objects.get(id=id)

    if actividad:
        actividad.delete()
        return redirect('/personas/modificar/%d/' % ci)

@user_passes_test(logeado, login_url='login')
def procesar_falla(request):
    if request.method == 'POST':
        persona_ci = request.POST['ci']
        persona = Persona.objects.get(ci=persona_ci)
        registrar_transaccion(persona, request.POST)

        return HttpResponse(
            json.dumps({'redirect_to': '/personas/{}'.format(persona_ci)}),
            content_type='application/json'
        )
    else:
        return redirect('/home')