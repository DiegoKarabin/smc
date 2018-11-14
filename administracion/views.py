from django.shortcuts import render,redirect,HttpResponse
from datetime import date
from django.contrib.auth.decorators import user_passes_test
from smc.views import logeado,is_audit
from administracion.models import *
from usuarios.models import BitacoraAcceso
import MySQLdb

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from wsgiref.util import FileWrapper

# Create your views here.

@user_passes_test(is_audit, login_url = '/usuarios/sin_permiso/')
def home(request):
    respaldo = configuracionBDA.objects.get(id = 1)
    return render(request, "administracion/home.html",{'respaldo' : respaldo})

@user_passes_test(is_audit, login_url = '/usuarios/sin_permiso/')
def configurarRespaldo(request):
    respaldo = configuracionBDA.objects.get(id = 1)
    if respaldo.respaldo == 1:
        respaldo.respaldo = 0
        p = Bitacora(descripcion = 'Apagado')
    else:
        respaldo.respaldo = 1
        p = Bitacora(descripcion = 'Encendido')
    respaldo.save()
    p.save()
    return redirect('/gestion/home')

def crearRespaldo(request):
    file_content = ''
    
    # Obtenemos la conexion con la base de datos.
    db = MySQLdb.connect(user='root', db='smc', passwd='', host='localhost')
    cursor = db.cursor()
    
    # Obtenemos los nombres de las tablas.
    cursor.execute('SHOW FULL TABLES FROM smc')
    tablas = [row[0] for row in cursor.fetchall()]
    
    for fila in tablas:
        # Obtenemos los registros de cada tabla
        cursor.execute('SELECT * FROM ' + fila)
        registros = cursor.fetchall()

        if len(registros):
            for registro in registros:
                file_content += "INSERT IGNORE INTO `" + fila + "` VALUES ("
                n = len(registro)
                i = 0
                for elemento in registro:
                    file_content += "'"+str(elemento)+"'"
                    if i < n - 1:
                        file_content += ","
                    i += 1;
                file_content += ");"
        
    db.close()
    name = 'Backup.'+ str(date.today()) + ".txt" 
    path = default_storage.save(name, ContentFile(file_content))
    # print(file_content)
    # file_path = os.path.join(settings.MEDIA_ROOT, path)
    # file_name = "Backup " + str(date.today()) + ".txt"
    # file = open(file_name,'w')
    # file.write(file_content)
    # file.close()
    bitacora = Bitacora(descripcion = 'Importacion')
    bitacora.save()
    # return redirect('/gestion/home/')
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}'.format(name)
    response['X-Sendfile'] = path
    return response

@user_passes_test(is_audit, login_url = '/usuarios/sin_permiso/')
def cambiarPeriodo(request):
    if request.method == 'POST':
        valor_nuevo = request.POST['periodo'] 
        valor = configuracionBDA.objects.get(id = 1)
        valor.periodo = valor_nuevo
        valor.save()
        bitacora = Bitacora(descripcion = 'CambioPeriodo')
        print("¡Correcto!")
        return redirect('/gestion/home')

@user_passes_test(is_audit, login_url = '/usuarios/sin_permiso')
def ver_bitacora(request):
    entradas = BitacoraAcceso.objects.all().order_by('-fecha', '-hora')

    return render(request, 'auditor/bitacora.html',
                  {
                      'titulo': 'Bitácora de Acceso',
                      'entradas': entradas
                  })