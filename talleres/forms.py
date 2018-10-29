from django import forms

class FormularioTaller(forms.Form):
	nombre = forms.CharField(
		label='Nombre del Grupo',
		widget=forms.TextInput(attrs={
			'placeholder': 'Introduzca un Nombre de Grupo',
			'class': 'form-control'
		}))
	tematica = forms.CharField(
		label='Temática',
		widget=forms.TextInput(attrs={
			'placeholder': 'Introduzca una Temática',
			'class': 'form-control'
		}))
	fecha_inicio = forms.DateField(
		label='Fecha de Inicio',
		widget=forms.DateInput(attrs={
			'placeholder': 'Introduzca una fecha',
			'class': 'form-control'
		}))
	sesiones = forms.IntegerField(
		label='Cantidad de sesiones',
		min_value=1,
		widget=forms.NumberInput(attrs={
			'placeholder': 'Introduzca una cantidad de sesiones',
			'class': 'form-control'
		}))
