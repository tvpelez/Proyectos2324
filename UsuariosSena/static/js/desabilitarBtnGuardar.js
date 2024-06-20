$(document).ready(function () {
	$('form').submit(function () {
		$('#submitBtn').prop('disabled', true);
		$('#submitBtn').text('GUARDANDO...');
	});
});