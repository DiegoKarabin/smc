from django import forms

from .models import Usuario


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['ci', 'nombre', 'apellido', 'profesion']

        widgets = {
            'ci': forms.TextInput(attrs={
                'placeholder': 'Introduzca una identificación',
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
            'profesion': forms.TextInput(attrs={
                'placeholder': 'Introduzca una profesión',
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['ci'])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('ci', 'nombre', 'apellido',
                  'profesion', 'is_active', 'is_admin')
        widgets = {
            'ci': forms.TextInput(attrs={
                'placeholder': 'Introduzca una identificación',
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
            'profesion': forms.TextInput(attrs={
                'placeholder': 'Introduzca una profesión',
                'class': 'form-control'
            }),
        }


class PasswordChangeForm(forms.Form):
    error_css_class = 'alert alert-danger'

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Introduzca una contraseña',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita la contraseña',
            'class': 'form-control'
        })
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')

        return password2