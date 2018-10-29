from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from smc.views import logeado

# Create your views here.

@user_passes_test(logeado, login_url = '/login/')
def home(request):
	return render(request, "administracion/home.html")