from django import forms

from . import models


class FormularioPersona(forms.ModelForm):

    class Meta:
        model = models.Persona
        fields = [
            'ci', 'nombre', 'apellido', 'sexo', 'condicion',
            'lugar_de_nacimiento', 'fecha_de_nacimiento',
            'estado_civil', 'nacionalidad', 'grado_de_institucion',
            'direccion', 'telefono', 'ocupacion', 'direccion_trabajo'
        ]

        widgets = {
            'ci': forms.TextInput(attrs={
                'placeholder': 'Introduzca un número de cédula',
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Introduzca un nombre',
                'class': 'form-control'
            }),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Introduzca un apellido',
                'class': 'form-control'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'lugar_de_nacimiento': forms.TextInput(attrs={
                'placeholder': 'Introduzca un lugar',
                'class': 'form-control'
            }),
            'fecha_de_nacimiento': forms.DateInput(attrs={
                'placeholder': 'Introduzca una fecha',
                'class': 'form-control'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nacionalidad': forms.TextInput(attrs={
                'placeholder': 'Introduzca una nacionalidad',
                'class': 'form-control'
            }),
            'grado_de_institucion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Introduzca una dirección',
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Introduzca un telefono',
                'class': 'form-control'
            }),
            'ocupacion': forms.TextInput(attrs={
                'placeholder': 'Introduzca una ocupación',
                'class': 'form-control'
            }),
            'direccion_trabajo': forms.TextInput(attrs={
                'placeholder': 'Introduzca una dirección',
                'class': 'form-control'
            }),
            'condicion': forms.Select(attrs={
                'class': 'form-control'
            })
        }
