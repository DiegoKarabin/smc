from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class CausasTest(LiveServerTestCase):

    def setUp(self):
        self.navegador = webdriver.Chrome()

    def tearDown(self):
        self.navegador.quit()

    def filtrar_elemento_por_atributos(self, coleccion, **atributos):
        try:
            return next(filter(lambda elemento: not any(
                elemento.get_attribute(k) != v for k, v in atributos.items()
            ), coleccion))
        except StopIteration:
            self.fail('Elemento con atributos ' +
                      repr(atributos) + ' no encontrado')

    def filtrar_elemento_por_texto(self, coleccion, texto):
        try:
            return next(filter(lambda elemento: elemento.text == texto,
                               coleccion))
        except StopIteration:
            self.fail('Elemento con texto "' + texto + '" no encontrado')

    def chequear_campo(self, label, placeholder):
        etiquetas = self.navegador.find_elements_by_tag_name('label')

        etiqueta = self.filtrar_elemento_por_texto(
            etiquetas, label)

        campo = self.navegador.find_element_by_id(
            etiqueta.get_attribute('for'))
        self.assertEquals(campo.get_attribute('placeholder'),
                          placeholder)

        return campo

    def test_crear_una_causa_y_ver_su_contenido(self):
        # Entra a la pagina de registro de causas
        self.navegador.get(self.live_server_url + '/causas/ingreso/')

        # En el titulo y el encabezado dice "Registrar una nueva causa"
        self.assertEquals('Registrar una nueva causa', self.navegador.title)
        texto_encabezado = self.navegador.find_element_by_tag_name('h1').text
        self.assertEquals('Registrar una nueva causa', texto_encabezado)

        # Un campo solicita el nro de expediente
        campo = self.chequear_campo('Nro. Expediente',
                                    'Introduzca un número de expediente')

        # Introduce "KPO1-S-2015-2231"
        campo.send_keys('KPO1-S-2015-2231')

        # Otro campo solicita el tribunal de procedencia
        campo = self.chequear_campo(
            'Tribunal de procedencia', 'Introduzca el tribunal de procedencia')

        # Introduce "Control 1"
        campo.send_keys('Control 1')

        # Otro campo solicita el tipo de delito
        campo = self.chequear_campo(
            'Tipo de delito', 'Introduzca el tipo de delito')

        # Introduce "Acoso u Hostigamiento"
        campo.send_keys('Acoso u Hostigamiento')

        # Otro campo pide la solicitud del tribunal
        campo = self.chequear_campo(
            'Solicitud del tribunal', 'Introduzca la solicitud del tribunal')

        # Introduce "Evaluacion Psico-social"
        campo.send_keys('Evaluación Psico-social')

        # Luego un campo le pide que introduzca la cédula de la victima
        campo = self.chequear_campo(
            'C.I. de la víctima', 'Introduzca un número de cédula')
        campo.send_keys('23456789')

        # Un campo le pide el nombre de la victima
        campo = self.chequear_campo(
            'Nombre de la víctima', 'Introduzca un nombre')
        campo.send_keys('María Pérez')

        # Un campo pide la edad
        campo = self.chequear_campo(
            'Edad de la víctima', 'Introduzca una edad')
        campo.send_keys('25')

        # Un campo le pide que introduzca la cédula del imputado
        campo = self.chequear_campo(
            'C.I. del imputado', 'Introduzca un número de cédula')
        campo.send_keys('19754952')

        # Otro campo le pide el nombre del imputado
        campo = self.chequear_campo(
            'Nombre del imputado', 'Introduzca un nombre')
        campo.send_keys('Juan Molina')

        # Un campo pide la edad
        campo = self.chequear_campo(
            'Edad del imputado', 'Introduzca una edad')
        campo.send_keys('34')

        # Hace click en el boton guardar
        boton = self.navegador.find_element_by_id('id_submit')
        self.assertEquals(boton.get_attribute('value'), 'Guardar')
        boton.click()

        # Es redireccionado a una pagina donde puede ver las causas guardadas
        self.assertEquals(self.navegador.current_url,
                          self.live_server_url + '/causas/')

        # Ahi ve un enlace con el nro de expediente de la causa
        # que acaba de registrar
        enlace = self.navegador.find_element_by_link_text('KPO1-S-2015-2231')

        # Hace click en el enlace
        enlace.click()

        # Es redireccionado a una pagina donde puede ver la informacion
        # de la causa registrada
        self.assertRegex(self.navegador.current_url, '/causas/.+/')
        contenido = self.navegador.find_element_by_tag_name('body').text
        self.assertIn('KPO1-S-2015-2231', contenido)
        self.assertIn('Control 1', contenido)
        self.assertIn('Acoso u Hostigamiento', contenido)
        self.assertIn('Evaluación Psico-social', contenido)
        self.assertIn('23456789', contenido)
        self.assertIn('María Pérez', contenido)
        self.assertIn('19754952', contenido)
        self.assertIn('Juan Molina', contenido)

        # Entra a la pagina para ver la lista de imputados
        self.navegador.get(self.live_server_url + '/imputados/')

        # Busca la cedula del imputado
        enlace = self.navegador.find_element_by_link_text('19754952')

        # Presiona el enlace y es llevado a una pagina con la informacion
        # de la persona
        enlace.click()
        self.assertRegex(self.navegador.current_url, '/imputados/\d+/')

        contenido = self.navegador.find_element_by_tag_name('body').text

        self.assertIn('Juan Molina', contenido)
        self.assertIn('34', contenido)

        # Presiona un enlace para registrar una actividad
        enlace = self.navegador.find_element_by_link_text(
            'Registrar actividad')
        enlace.click()

        # Un cuadro de texto le pide que introduzca la descripcion de la
        # actividad
        campo = self.chequear_campo(
            'Descripción de la actividad', 'Introduzca una descripción')

        # Introduce pedir cita
        campo.send_keys('Pedir cita')

        # Presiona el boton registrar y registra la actividad
        boton = self.navegador.find_element_by_id('id_submit')
        self.assertEquals(boton.get_attribute('value'), 'Registrar')
        boton.click()

        # Es redireccionado a la pagina con la informacion del imputado
        self.assertRegex(self.navegador.current_url, '/imputados/\d+/')

        # Ahora se dirige a la pagina de la informacion de las victimas
        self.navegador.get(self.live_server_url + '/victimas/')

        # Busca la cedula de la victima
        enlace = self.navegador.find_element_by_link_text('23456789')

        # Presiona el enlace y es llevado a una pagina con informacion
        # de la persona
        enlace.click()
        self.assertRegex(self.navegador.current_url, '/victimas/\d+')

        contenido = self.navegador.find_element_by_tag_name('body').text

        self.assertIn('María Pérez', contenido)
        self.assertIn('25', contenido)

        # Presiona un enlace para registrar una actividad
        enlace = self.find_element_by_link_text('Registrar actividad')
        enlace.click()

        # Un cuadro de texto le pide que introduzca la descripcion de la
        # actividad
        campo = self.chequear_campo(
            'Descripción de la actividad', 'Introduzca una descripción')

        # Introduce pedir cita
        campo.send_keys('Pedir cita')

        # Presiona el boton registrar y registra la actividad
        boton = self.navegador.find_element_by_id('id_submit')
        self.assertEquals(boton.get_attribute('value'), 'Registrar')
        boton.click()

        # Es redireccionado a la pagina con la informacion de la victima
        self.assertRegex(self.navegador.current_url, '/victimas/\d+/')

        self.fail('Terminar la prueba')
