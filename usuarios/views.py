from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from .models import Usuario, Pregunta, PreguntaUsuario
from . import forms
from smc.views import logeado

# Create your views here.

def es_admin(user):
    return user.is_admin

def es_mi_perfil(user, ci):
    return user.is_admin or user.ci == ci

@user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def ver_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuarios.html',
      {
        'usuarios': usuarios
      })

@user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def agregar_usuario(request):
    formulario = forms.UserCreationForm()

    if request.method == 'POST':
        formulario = forms.UserCreationForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('/usuarios/')

    return render(request, 'usuarios/formulario_usuario.html',
                  {
                      'formulario': formulario,
                      'titulo': 'Agregar usuario'
                  })

# @user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def ver_usuario(request, ci):
    if es_admin or request.user.ci == ci:
        try:
            usuario = Usuario.objects.get(ci=ci)
        except:
            return render(request, 'usuarios/no_existe.html')
        return render(request, 'usuarios/info_usuario.html',
          {
            'usuario_consultado': usuario
          })
    else:
        return redirect('/usuarios/sin_permiso')

@user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def buscar(request):
    q = request.GET.get('identificacion', '')

    if q:
        return redirect('/usuarios/ver/' + q + '/')
    else:
        return redirect('/usuarios/')

# @user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def modificar_usuario(request, ci):
    if es_admin(request.user) or request.user.ci == ci:
        usuario = Usuario.objects.get(ci=ci)

        if es_admin(request.user):
            formulario = forms.UserChangeForm(instance=usuario)
        else:
            formulario = forms.UserChangeFormNoAdmin(instance=usuario)

        if request.method == 'POST':
            if es_admin(request.user):
                formulario = forms.UserChangeForm(request.POST, instance=usuario)
            else:
                # data = dict(request.POST)
                # data.update(is_active=True)
                formulario = forms.UserChangeFormNoAdmin(request.POST, instance=usuario)

            if formulario.is_valid():
                formulario.save()
                return redirect('/usuarios/ver/' + usuario.ci + '/')

        return render(request, 'usuarios/formulario_usuario.html',
                      {
                          'formulario': formulario,
                          'titulo': 'Modificar usuario ' + usuario.get_full_name()
                      })
    else:
        return redirect('/usuarios/sin_permiso/')

@user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def eliminar_usuario(request, ci):
    usuario = Usuario.objects.get(ci=ci)

    if usuario:
        usuario.delete()

    return redirect('/usuarios/')

@user_passes_test(es_admin, login_url='/usuarios/sin_permiso/')
def inhabilitar_usuario(request, ci):
    usuario = Usuario.objects.get(ci=ci)

    if usuario:
        usuario.is_active = not usuario.is_active
        usuario.save()

        return redirect('/usuarios/ver/' + ci + '/')
    else:
        return redirect('/usuarios/')

@user_passes_test(logeado, login_url='/login/')
def cambiar_clave(request):
    if request.user.is_security_question_setted:
        try:
            if not request.GET['validado']:
                return redirect('/usuarios/validar_preguntas?next=/usuarios/cambiar_clave/')
        except Exception:
                return redirect('/usuarios/validar_preguntas?next=/usuarios/cambiar_clave/')

    formulario = forms.PasswordChangeForm()

    if request.method == 'POST':
        formulario = forms.PasswordChangeForm(
            request.POST)

        if formulario.is_valid():
            clave = formulario.cleaned_data['password2']
            request.user.set_password(clave)
            request.user.is_password_setted = True
            request.user.save()
            return redirect('/login/')

    return render(request, 'usuarios/cambiar_clave.html',
                  {
                      'formulario': formulario,
                      'titulo': 'Cambiar Contraseña'
                  })

@user_passes_test(logeado, login_url='/login/')
def preguntas_seguridad(request):
    if request.method == 'POST':
        def relate_question_user(question_index, user, answer):
            question = Pregunta.objects.get(id=question_index)
            qu = PreguntaUsuario(usuario=user, pregunta=question)
            qu.setRespuesta(answer)
            qu.save()

        relate_question_user(request.POST['question1'], request.user, request.POST['answer1'])
        relate_question_user(request.POST['question2'], request.user, request.POST['answer2'])

        request.user.is_security_question_setted = True
        request.user.save()
        return redirect('/home/')

    preguntas = Pregunta.objects.all()

    return render(request, 'usuarios/formulario_preguntas.html',
                  {
                      'titulo': 'Establecer preguntas de seguridad',
                      'preguntas': preguntas,
                  })

@user_passes_test(logeado, login_url='/login/')
def validar_preguntas(request):
    errores = {}

    if request.method == 'POST':
        pu = PreguntaUsuario.objects.filter(usuario=request.user)
        pregunta1 = pu[0]
        pregunta2 = pu[1]

        if not pregunta1.es_respuesta_correcta(request.POST['respuesta1']):
            errores['pregunta1'] = 'La respuesta que ingreso es incorrecta'

        if not pregunta2.es_respuesta_correcta(request.POST['respuesta2']):
            errores['pregunta2'] = 'La respuesta que ingreso es incorrecta'

        if not errores:
            return redirect(request.POST['next'] + '?validado=1')

    preguntas = request.user.preguntas.all()

    return render(request, 'usuarios/formulario_validacion_preguntas.html',
                  {
                      'titulo': 'Validar preguntas de seguridad',
                      'pregunta1': preguntas[0],
                      'pregunta2': preguntas[1],
                      'next': request.GET['next'],
                      'errores': errores,
                  })

def sin_permiso(request):
    return render(request, 'usuarios/sin_permiso.html')
