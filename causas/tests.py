from django.test import TestCase
from django.urls import resolve

from causas.views import nueva_causa, ver_causas
from causas.models import Causa, Imputado, Victima

# Create your tests here.

victima_prueba = {
    'nombre': 'María',
    'apellido': 'Pérez',
    'ci': '23456789',
    'edad': 25
}

imputado_prueba = datos = {
    'nombre': 'Juan',
    'apellido': 'Molina',
    'ci': '19754952',
    'edad': 34
}

causa_prueba_post = {
    'nro_expediente': 'KPO1-S-2015-2231',
    'procedencia': 'Circuito 1',
    'delito': 'Acoso Verbal',
    'solicitud': 'Evaluación Psico-social',
    'ci_victima': victima_prueba['ci'],
    'nombre_victima': victima_prueba['nombre'],
    'edad_victima': victima_prueba['edad'],
    'ci_imputado': imputado_prueba['ci'],
    'nombre_imputado': imputado_prueba['nombre'],
    'edad_imputado': imputado_prueba['edad'],
}

causa_prueba = {
    'nro_expediente': 'KPO1-S-2015-2254',
    'procedencia': 'Circuito 1',
    'delito': 'Acoso Verbal',
    'solicitud': 'Evaluación Psico-social',
    'victima': Victima.objects.create(**victima_prueba),
    'imputado': Imputado.objects.create(**imputado_prueba),
}


class NuevasCausasTest(TestCase):

    def test_url_ingresos_retorna_la_vista_correcta(self):
        respuesta = resolve('/causas/ingreso/')
        self.assertEquals(respuesta.func, nueva_causa)

    def test_nueva_causa_retorna_html(self):
        respuesta = self.client.get('/causas/ingreso/')
        self.assertTemplateUsed(respuesta, 'formulario_causas.html')

    def test_vista_puede_guardar_una_solicitud_POST(self):
        self.client.post('/causas/ingreso/', data=causa_prueba_post)

        self.assertEquals(Causa.objects.count(), 1)

    def test_no_guarda_datos_vacios(self):
        self.client.post('/causas/ingreso/',
                         data={
                             'nro_expediente': '',
                             'procedencia': '',
                             'delito': '',
                             'solicitud': '',
                             'ci_victima': '',
                             'nombre_victima': '',
                             'edad_victima': '',
                             'ci_imputado': '',
                             'nombre_imputado': '',
                             'edad_imputado': '',
                         })

        self.assertEquals(Causa.objects.count(), 0)

    def test_redirige_despues_de_POST(self):
        respuesta = self.client.post(
            '/causas/ingreso/', data=causa_prueba_post)
        self.assertRedirects(respuesta, '/causas/')


class VerCausas(TestCase):

    def test_existe_url_para_ver_causas_registradas(self):
        respuesta = resolve('/causas/')
        self.assertEquals(respuesta.func, ver_causas)

    def test_vista_retorna_html(self):
        respuesta = self.client.get('/causas/')
        self.assertTemplateUsed(respuesta, 'causas.html')

    def test_muestra_todas_las_causas_registradas(self):
        victima = Victima.objects.create(ci='3424')
        imputado = Imputado.objects.create(ci='87654')
        causa1 = Causa.objects.create(
            nro_expediente='1234', victima=victima, imputado=imputado)
        causa2 = Causa.objects.create(
            nro_expediente='9876', victima=victima, imputado=imputado)

        respuesta = self.client.get('/causas/')
        self.assertContains(respuesta, causa1.nro_expediente)
        self.assertContains(respuesta, causa2.nro_expediente)

    def test_muestra_la_informacion_de_una_causa_especifica(self):
        causa = Causa.objects.create(**causa_prueba)

        respuesta = self.client.get('/causas/' + causa.nro_expediente + '/')
        self.assertContains(respuesta, causa.nro_expediente)
        self.assertContains(respuesta, causa.procedencia)
        self.assertContains(respuesta, causa.delito)
        self.assertContains(respuesta, causa.solicitud)

        otra_causa = Causa.objects.create(
            nro_expediente='1234',
            victima=Victima.objects.create(ci='5634'),
            imputado=Imputado.objects.create(ci='32424'))
        respuesta = self.client.get(
            '/causas/' + otra_causa.nro_expediente + '/')
        self.assertContains(respuesta, otra_causa.nro_expediente)


class ModeloVictimaTest(TestCase):

    def test_puede_guardar_una_victima(self):
        Victima.objects.create(**victima_prueba)
        self.assertEquals(Victima.objects.count(), 1)

    def test_ver_todos_las_victimas_registradas(self):
        victima = Victima.objects.create(**victima_prueba)
        respuesta = self.client.get('/victimas/')
        self.assertContains(respuesta, victima.ci)

    def test_ver_la_informacion_de_una_victima(self):
        victima = Victima.objects.create(**victima_prueba)
        respuesta = self.client.get('/victimas/' + victima.ci + '/')
        self.assertContains(respuesta, victima.ci)
        self.assertContains(respuesta, victima.nombre)
        self.assertContains(respuesta, victima.edad)



class ModeloImputadoTest(TestCase):

    def test_puede_guardar_un_imputado(self):
        Imputado.objects.create(**imputado_prueba)
        self.assertEquals(Imputado.objects.count(), 1)

    def test_ver_todos_los_imputados_registrados(self):
        imputado = Imputado.objects.create(**imputado_prueba)
        respuesta = self.client.get('/imputados/')
        self.assertContains(respuesta, imputado.ci)

    def test_ver_la_informacion_de_un_imputado(self):
        imputado = Imputado.objects.create(**imputado_prueba)
        respuesta = self.client.get('/imputados/' + imputado.ci + '/')
        self.assertContains(respuesta, imputado.ci)
        self.assertContains(respuesta, imputado.nombre)
        self.assertContains(respuesta, imputado.edad)