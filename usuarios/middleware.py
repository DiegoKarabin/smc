from django.shortcuts import redirect
from usuarios.views import cambiar_clave, preguntas_seguridad

class ConfigurationMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.user.is_authenticated:
			# if its password is not setted
			if not request.user.is_password_setted:
				return cambiar_clave(request)

			# if doesn't have security question
			if not request.user.is_security_question_setted:
				return preguntas_seguridad(request)
		
		return self.get_response(request)
