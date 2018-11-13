from django.shortcuts import render,redirect,HttpResponse
from datetime import date
from django.contrib.auth.decorators import user_passes_test
from smc.views import logeado,is_audit
from administracion.models import *
import MySQLdb
import os,tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import datetime

from django.views.static import serve
from django.utils.encoding import smart_str

from wsgiref.util import FileWrapper

from django.views.static import serve
from django.utils import timezone

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
	respaldo = configuracionBDA.objects.get(id = 1)
	respaldo.uitima_exportacion = datetime.datetime.now()
	respaldo.save()

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

	respaldo = configuracionBDA.objects.get(id = 1)
	respaldo.ultima_exportacion = datetime.datetime.now()
	respaldo.save()

	name = 'Backup.'+ str(date.today()) + ".sql"
	file = open(name,'w')
	file.write(file_content)
	file.close()
	filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/" + name
	filepath = filepath.replace('\\','/')
	return serve(request, os.path.basename(filepath), os.path.dirname(filepath))



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


def restauracion(request):
	respaldo = configuracionBDA.objects.get(id = 1)
	respaldo.ultima_importacion = datetime.datetime.now()
	respaldo.save()
	return render(request, "administracion/restaurar.html")

