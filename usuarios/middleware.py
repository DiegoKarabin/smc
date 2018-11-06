class ConfigurationMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# if its password is not setted
		if request.user.is_password_setted:
			return redirect('/usuarios/cambiar_clave')

		# if doesn't have security question
		if request.user.is_security_question_setted:
			return redirect('/usuarios/preguntas')

		response = self.get_response(request)

		return response