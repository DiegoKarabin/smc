from django.shortcuts import render,redirect,HttpResponse
from datetime import date
from django.contrib.auth.decorators import user_passes_test
from smc.views import logeado
from administracion.models import *
import MySQLdb

from wsgiref.util import FileWrapper

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
				file_content += "INSERT INTO `" + fila + "` VALUES ("
				n = len(registro)
				i = 0
				for elemento in registro:
					file_content += "'"+str(elemento)+"'"
					if i < n - 1:
						file_content += ","
					i += 1;
				file_content += ");"
		
	print(file_content)
	db.close()
	file_name = "Backup " + str(date.today()) + ".sql"
	file = open(file_name,'w')
	file.write("Hola mundo")
	file.close()
	response = HttpResponse(content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
	response['X-Sendfile'] = file
	return response
