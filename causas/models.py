from django.db import models
from datetime import date, datetime, timedelta

from personas.models import Persona

# Create your models here.


class Causa(models.Model):
    PENDIENTE = 'Pendiente'
    ACTIVO = 'Activo'
    CULMINADO = 'Culminado'
    OPCIONES_ESTADO = (
        (PENDIENTE, 'Pendiente'),
        (ACTIVO, 'Activo'),
        (CULMINADO, 'Culminado')
    )

    EVA_PSICOLOGICA = 'Evaluación Psicológica'
    EVA_SOCIAL = 'Evaluación Social'
    EVA_PSICO_SOCIAL = 'Evaluación Psico-Social'
    TRIAJE = 'Triaje'
    TALLER = 'Taller'
    ORIENTACION = 'Orientación'
    PRUEBA_ANTICIPADA = 'Prueba Anticipada'
    OPCIONES_SOLICITUDES = (
        (EVA_PSICOLOGICA, 'Evaluación Psicológica'),
        (EVA_SOCIAL, 'Evaluación Social'),
        (EVA_PSICO_SOCIAL, 'Evaluación Psico-Social'),
        (TRIAJE, 'Triaje'),
        (TALLER, 'Taller'),
        (ORIENTACION, 'Orientación'),
        (PRUEBA_ANTICIPADA, 'Prueba Anticipada')
    )

    CONTROL_1 = 'Control 1'
    CONTROL_2 = 'Control 2'
    CONTROL_3 = 'Control 3'
    JUICIO_1 = 'Juicio 1'
    JUICIO_2 = 'Juicio 2'
    EJECUCION = 'Ejecución'
    OTROS = 'Otros Tribunales'

    OPCIONES_PROCEDENCIA = (
        (CONTROL_1, 'Control 1'),
        (CONTROL_2, 'Control 2'),
        (CONTROL_3, 'Control 3'),
        (JUICIO_1, 'Juicio 1'),
        (JUICIO_2, 'Juicio 2'),
        (EJECUCION, 'Ejecución'),
        (OTROS, 'Otros Tribunales')
    )

    PSICOLOGICA = 'Violencia Psicológica'
    ACOSO_HOST = 'Acoso u Hostigamiento'
    AMENAZA = 'Amenaza'
    FISICA = 'Violencia Física'
    FISICA_AGR = 'Violencia Física Agravada'
    SEXUAL = 'Violencia Sexual'
    ACT_CARN_VICT_VUL = 'Acto Carnal con Víctima Vulnerable'
    ACT_LASC = 'Actos Lascivos'
    PROST_FORZADA = 'Prostitución Forzada'
    ESCLAVITUD_SEXUAL = 'Esclavitud Sexual'
    ACOSO_SEXUAL = 'Acoso Sexual'
    LABORAL = 'Violencia Laboral'
    PATRIM_ECO = 'Violencia Patrimonial y Económica'
    OBSTETRICA = 'Violencia Obstétrica'
    ESTERIL_FORZADA = 'Esterilización Forzada'
    OFENSA_PUBLICA = 'Ofensa Pública'
    INSTITUCIONAL = 'Violencia Institucional'
    TRAF_ILIC_NNA_ADO_MUJ = (
        'Tráfico Ilícito de Niñas, Adolescentes y Mujeres')
    TRATA_MUJ_NNA_ADO = 'Trata de Mujeres, Niñas y Adolescentes'
    FEMICIDIO = 'Femicidio'
    FEMICIDIO_AGR = 'Femicidio Agravado'
    IND_AL_SUICIDIO = 'Inducción al Suicidio'
    OBLG_AVISO = 'Obligación de Aviso'
    OBLG_TRAM_DEN = 'Obligación de Trámites de Denuncia'
    OBLG_IMP_CORREC = 'Obligación de Implementación de Correctivos'
    REINCIDENCIA = 'Reincidencia'
    OTRO_DELITO = 'Otros'
    OPCIONES_DELITO = (
        (PSICOLOGICA, 'Violencia Psicológica'),
        (ACOSO_HOST, 'Acoso u Hostigamiento'),
        (AMENAZA, 'Amenaza'),
        (FISICA, 'Violencia Física'),
        (FISICA_AGR, 'Violencia Física Agravada'),
        (SEXUAL, 'Violencia Sexual'),
        (ACT_CARN_VICT_VUL, 'Acto Carnal con Víctima Vulnerable'),
        (ACT_LASC, 'Actos Lascivos'),
        (PROST_FORZADA, 'Prostitución Forzada'),
        (ESCLAVITUD_SEXUAL, 'Esclavitud Sexual'),
        (ACOSO_SEXUAL, 'Acoso Sexual'),
        (LABORAL, 'Violencia Laboral'),
        (PATRIM_ECO, 'Violencia Patrimonial y Económica'),
        (OBSTETRICA, 'Violencia Obstetrica'),
        (ESTERIL_FORZADA, 'Esterilización Forzada'),
        (OFENSA_PUBLICA, 'Ofensa Pública'),
        (INSTITUCIONAL, 'Violencia Institucional'),
        (TRAF_ILIC_NNA_ADO_MUJ,
            'Tráfico Ilicito de Niñas, Adolescentes y Mujeres'),
        (TRATA_MUJ_NNA_ADO, 'Trata Mujeres, Niña y Adolescentes'),
        (FEMICIDIO, 'Femicidio'),
        (FEMICIDIO_AGR, 'Femicidio Agravado'),
        (IND_AL_SUICIDIO, 'Inducción al Suicidio'),
        (OBLG_AVISO, 'Obligación de Aviso'),
        (OBLG_TRAM_DEN, 'Obligación de Trámites de Denuncia'),
        (OBLG_IMP_CORREC, 'Obligación de Implementación de Correctivos'),
        (OTRO_DELITO, 'Otros')
    )

    nro_expediente = models.CharField(
        max_length=20, default='', primary_key=True)
    procedencia = models.CharField(max_length=16, choices=OPCIONES_PROCEDENCIA)
    solicitud = models.CharField(max_length=23, choices=OPCIONES_SOLICITUDES)
    delito = models.CharField(max_length=50, choices=OPCIONES_DELITO)
    fecha_ingreso = models.DateField(default=date.today)
    personas = models.ManyToManyField(Persona)
    estado = models.CharField(max_length=9, choices=OPCIONES_ESTADO,
        default=PENDIENTE)
    edit = models.BooleanField(default=False)
    is_editing = models.CharField(max_length=9, default=0)


class Actividad(models.Model):
    SOLICITUD_CITA = 'Solicitud de Cita'
    TRIAJE_EVALUACION = 'Triaje y Evaluación'
    CONTENCION = 'Contención'
    NOTF_RECIBIDA = 'Notificación Recibida'
    NOTF_ENVIADA = 'Notificación Enviada'
    REMISION_INFORME = 'Remisión de Informe'
    VISITA_DOM = 'Visita Domiciliaria'
    ORIENTACION = 'Orientación'
    AUDIENCIA = 'Audiencia'
    PRUEBA_ANT = 'Prueba Anticipada'
    REF_SALUD = 'Referencia a Centro de Salud'
    CARTA_CULM = 'Carta de Culminación'
    LLAMADA_TELF = 'Llamada Telefónica'
    TALLER = 'Taller'
    OPCIONES_ACTIVIDAD = (
        (SOLICITUD_CITA, 'Solicitud de Cita'),
        (TRIAJE_EVALUACION, 'Triaje y Evaluación'),
        (CONTENCION, 'Contención'),
        (NOTF_RECIBIDA, 'Notificación Recibida'),
        (NOTF_ENVIADA, 'Notificación Enviada'),
        (REMISION_INFORME, 'Remision de Informe'),
        (VISITA_DOM, 'Visita Domiciliaria'),
        (ORIENTACION, 'Orientación'),
        (AUDIENCIA, 'Audiencia'),
        (PRUEBA_ANT, 'Prueba Anticipada'),
        (REF_SALUD, 'Referencia a Centro de Salud'),
        (CARTA_CULM, 'Carta de Culminación'),
        (LLAMADA_TELF, 'Llamada Telefónica'),
        (TALLER, 'Taller')
    )
    descripcion = models.CharField(max_length=28, choices=OPCIONES_ACTIVIDAD)
    participante = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.today)


class Triaje(models.Model):
    ORIENTACION = 'Orientación'
    EVALUACION = 'Evaluación'
    REMISION_EXTERNA = 'Remisión Externa'
    OPCIONES_ACCION = (
        (ORIENTACION, 'Orientación'),
        (EVALUACION, 'Evaluación'),
        (REMISION_EXTERNA, 'Remisión Externa')
    )

    ASESORIA_JURIDICA = 'Asesoría Jurídica'
    TRABAJO_SOCIAL = 'Trabajo Social'
    MEDICINA = 'Medicina'
    PSICOLOGIA = 'Psicología'
    EDUCACION = 'Educación'
    OPCIONES_DERIVACION = (
        (ASESORIA_JURIDICA, 'Asesoría Jurídica'),
        (TRABAJO_SOCIAL, 'Trabajo Social'),
        (MEDICINA, 'Medicina'),
        (PSICOLOGIA, 'Psicología'),
        (EDUCACION, 'Educación'),
    )

    causa = models.OneToOneField(Causa, on_delete=models.CASCADE, default=None)
    genograma_imputado = models.TextField(blank=True)
    genograma_victima = models.TextField(blank=True)
    testimonio_imputado = models.TextField(blank=True)
    testimonio_victima = models.TextField(blank=True)
    impresion_diagnostica = models.TextField(blank=True)
    modalidad = models.CharField('Modalidad de Intervención',
                                 choices=OPCIONES_ACCION, max_length=16)
    observaciones = models.TextField(blank=True)
    derivacion = models.CharField('Derivacion a equipo interdisciplinario',
                                  choices=OPCIONES_DERIVACION, max_length=17)
    proxima_cita = models.DateField(
        default=(date.today() + timedelta(days=7)))
    atendido_por = models.CharField(max_length=50)

class Movimiento(models.Model):
    descripcion = models.CharField(max_length=28)
    causa = models.ForeignKey(Causa, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=datetime.today)
    realizado_por = models.CharField(max_length=50)
