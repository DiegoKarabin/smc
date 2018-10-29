from django import forms
from . import models


class FormularioCausa(forms.ModelForm):

    class Meta:
        model = models.Causa
        fields = ['nro_expediente', 'procedencia', 'solicitud',
                  'delito']
        widgets = {
            'nro_expediente': forms.TextInput(attrs={
                'placeholder': 'Introduzca un número de expediente',
                'class': 'form-control'
            }),
            'procedencia': forms.Select(attrs={
                'placeholder': 'Introduzca el tribunal de procedencia',
                'class': 'form-control'
            }),
            'solicitud': forms.Select(attrs={
                'placeholder': 'Introduzca la solicitud del tribunal',
                'class': 'form-control'
            }),
            'delito': forms.Select(attrs={
                'placeholder': 'Introduzca el tipo de delito',
                'class': 'form-control'
            })
        }


class FormularioTriaje(forms.ModelForm):

    class Meta:
        model = models.Triaje
        fields = ['genograma_imputado', 'genograma_victima',
                  'testimonio_imputado', 'testimonio_victima',
                  'impresion_diagnostica', 'modalidad',
                  'observaciones', 'derivacion', 'proxima_cita']
        widgets = {
            'genograma_imputado': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'genograma_victima': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'testimonio_imputado': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'testimonio_victima': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'impresion_diagnostica': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'derivacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'proxima_cita': forms.DateInput(attrs={
                'class': 'form-control'
            })
        }


class FormularioActividad(forms.ModelForm):

    class Meta:
        model = models.Actividad
        fields = ['descripcion']
        exclude = ['participante', 'fecha']
        widgets = {
            'descripcion': forms.Select(attrs={
                'class': 'form-control'
            })
        }
