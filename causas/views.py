from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from smc.views import logeado
from personas.models import Persona
from .models import Causa, Actividad, Triaje
from .forms import FormularioCausa, FormularioTriaje, FormularioActividad

# Create your views here.
 

@user_passes_test(logeado, login_url='/login/')
def nueva_causa(request):
    formulario = FormularioCausa()

    if request.method == 'POST':
        formulario = FormularioCausa(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('/causas/')

    return render(request, 'formulario.html',
                  {
                      'formulario': formulario,
                      'titulo': 'Registrar una nueva causa',
                  })


@user_passes_test(logeado, login_url='/login/')
def ver_causas(request):
    causas = Causa.objects.all()
    return render(request, 'causas/causas.html',
      {
        'causas': causas,
      })


@user_passes_test(logeado, login_url='/login/')
def ver_causa(request, nro_expediente):
    try:
        causa = Causa.objects.get(nro_expediente=nro_expediente)
    except:
        return render(request, 'causas/no_existe.html')

    victimas = causa.personas.get_queryset().filter(condicion=Persona.VICTIMA)
    imputados = causa.personas.get_queryset().filter(
        condicion=Persona.IMPUTADO)
    return render(request, 'causas/info.html',
                  {
                      'causa': causa,
                      'victimas': victimas,
                      'imputados': imputados,
                  })

@user_passes_test(logeado, login_url='/login/')
def buscar(request):
    q = request.GET.get('nro_expediente', '')

    if q:
        return redirect('/causas/ver/' + q + '/')
    else:
        return redirect('/causas/')

@user_passes_test(logeado, login_url='/login/')
def agregar_actividad(request):
    if request.method == 'POST' and all(request.POST.values()):
        formulario = FormularioActividad()
        ci = request.POST.get('ci', '')
        return render(request, 'causas/formulario_actividad.html',
          {
            'ci': ci,
            'formulario': formulario
          })
    return redirect('/causas/')


@user_passes_test(logeado, login_url='/login/')
def registrar_actividad(request):
    if request.method == 'POST' and all(request.POST.values()):
        ci = request.POST.get('ci', '')
        descripcion = request.POST.get('descripcion', '')
        persona = Persona.objects.get(ci=ci)
        Actividad.objects.create(
            descripcion=descripcion,
            participante=persona,
        )

        return redirect('/personas/' + ci + '/')
    return redirect('/causas/')


@user_passes_test(logeado, login_url='/login/')
def modificar_causa(request, nro_expediente):
    causa = Causa.objects.get(nro_expediente=nro_expediente)

    if causa.edit == False:
        causa.edit = True
        causa.is_editing = request.user.ci
        causa.save()

    else:
        if causa.edit == True and request.user.ci == causa.is_editing:

          if request.method == 'POST':
              formulario = FormularioCausa(request.POST, instance=causa)

              if formulario.is_valid():
                  causa.edit = False
                  causa.save()
                  formulario.save()
                  return redirect('/causas/ver/' + nro_expediente + '/')

          formulario = FormularioCausa(instance=causa)
          victimas = causa.personas.get_queryset().filter(condicion=Persona.VICTIMA)
          imputados = causa.personas.get_queryset().filter(
              condicion=Persona.IMPUTADO)

          return render(request, 'causas/formulario_causa.html',
                        {
                            'formulario': formulario,
                            'titulo': 'Modificar ' + nro_expediente,
                            'nro_expediente': nro_expediente,
                            'victimas': victimas,
                            'imputados': imputados
                        })
        else:
          return redirect('/edit_bloqueado.html')


@user_passes_test(logeado, login_url='/login')
def remover_persona(request, ci, nro_expediente):
    causa = Causa.objects.get(nro_expediente=nro_expediente)
    persona = Persona.objects.get(ci=ci)

    if causa and persona:
        causa.personas.remove(persona)
        return redirect('/causas/modificar/' + nro_expediente + '/')

    return redirect('/causas/ver/' + nro_expediente + '/')


@user_passes_test(logeado, login_url='/login/')
def eliminar_causa(request, nro_expediente):
    causa = Causa.objects.get(nro_expediente=nro_expediente)

    if causa:
        causa.delete()

    return redirect('/causas/')


@user_passes_test(logeado, login_url='/login/')
def agregar_triaje(request, nro_expediente):
    causa = Causa.objects.get(nro_expediente=nro_expediente)

    if causa:
        formulario = FormularioTriaje()
        if request.method == 'POST':
            formulario = FormularioTriaje(request.POST)

            if formulario.is_valid():
                datos = formulario.cleaned_data
                Triaje.objects.create(
                    causa=causa,
                    atendido_por=request.user.get_full_name(),
                    **datos)
                return redirect('/causas/ver/' + nro_expediente + '/')

        return render(request, 'formulario.html',
                      {
                          'formulario': formulario,
                          'titulo': 'Triaje',
                      })

    return redirect('/causas/')
