from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Usuario
from .forms import UserCreationForm, UserChangeForm


# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('ci', 'nombre', 'apellido', 'profesion')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('ci', 'password')}),
        ('Informacion personal',
         {'fields': ('nombre', 'apellido', 'profesion')}),
        ('Permisos', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('ci', 'nombre', 'apellido', 'profesion', 'password1',
                       'password2')}),
    )

    search_fields = ('ci', 'nombre', 'apellido')
    ordering = ('ci', 'nombre', 'apellido')
    filter_horizontal = ()

admin.site.register(Usuario, UserAdmin)
