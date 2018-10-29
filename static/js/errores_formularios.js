(function() {
	errores = document.getElementsByClassName('errorlist');

	if (errores.length)
		for (var i = errores.length - 1; i >= 0; i--) {
			var nodos = errores[i].childNodes;
			for (var j = nodos.length - 1; j >= 0; j--) {
				nodos[j].setAttribute('class', 'alert alert-danger');
				nodos[j].setAttribute('role', 'alert');
			}

			errores[i].style = "list-style: none; padding-left: 0; margin-top: 10px;";
		}
}())