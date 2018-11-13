from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from smc.views import logeado
from causas.models import Causa, Actividad
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
            causa.personas.create(**persona)

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


@user_passes_test(logeado, login_url='/login/')
def modificar_persona(request, ci):
    persona = Persona.objects.get(ci=ci)

    if persona.edit == False:
        persona.edit = True
        persona.is_editing = request.user.ci
        persona.save()

    else:
        if persona.edit == True and request.user.ci == persona.is_editing:

          if request.method == 'POST':
              formulario = FormularioPersona(request.POST, instance=persona)

              if formulario.is_valid():
                  persona.edit = False
                  persona.save()
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
