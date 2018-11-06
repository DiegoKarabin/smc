function passwordLength(password) {
	return password.length >= 8 && password.length <= 15;
}

function validateMatchesQty(password, pattern, length) {
	var matches = password.match(pattern);

	if (matches) {
		return matches.length > length;
	}

	return false;
}

function moreThan2Letters(password) {
	return validateMatchesQty(password, /([a-zA-Z])/g, 2);
}

function moreThan2Numbers(password) {
	return validateMatchesQty(password, /\d/g, 2);
}

function notConsecutiveNumbers(password) {
	return !/\d{2,}/g.test(password);
}

function hasNumbers(password) {
	return /\d/.test(password);
}

function hasLetters(password) {
	return /[a-zA-Z]/.test(password);
}

function notBlankSpaces(password) {
	return !/\s/.test(password);
}

var specialCharacters = '%_\\-&#=\\$@';

function hasSpecialCharacters(password) {
	var pattern = new RegExp('[' + specialCharacters + ']');
	return pattern.test(password);
}

function notConsecutiveSpecialCharacters(password) {
	var pattern = new RegExp('[' + specialCharacters + ']{2,}', 'g');
	return !pattern.test(password);
}

function notOnlyNumbers(password) {
	return hasLetters(password) || hasSpecialCharacters(password);
}

function notOnlyLetters(password) {
	return hasNumbers(password) || hasSpecialCharacters(password);
}

function moreThan2SpecialCharacters(password) {
	var pattern = new RegExp('([' + specialCharacters + '])', 'g');
	return validateMatchesQty(password, pattern, 2);
}