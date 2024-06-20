// DESABILITAR CAMPOS SI ESTA AGOTADO EL ELEMENTO
function actualizarEstadoFormulario(agotado) {
    var campos = [
        '#nombreElementoInput',
        '#disponiblesInput',
        '#cantidadElemento',
        '#observaciones_prestamo',
        'input[type="file"]',
        'button[type="submit"]'
    ];

    campos.forEach(function (selector) {
        $(selector).prop('disabled', agotado);
        $(selector).css('background-color', agotado ? '#e0e0e0' : '');
    });
}

$(document).ready(function () {
    $('#idElementoInput').on('input', function () {
        var consumibleId = $(this).val();

        if (consumibleId) {
            $.ajax({
                url: '/get_element_consum_info',
                type: 'GET',
                data: { 'consumibleId': consumibleId },
                success: function (response) {
                    // Actualizar los campos
                    $('#nombreElementoInput').val(response.nombreElemento);

                    // Actualizar el estado del formulario basado en la disponibilidad
                    if (response.disponible <= 0) {
                        actualizarEstadoFormulario(true); // Deshabilitar campos
                        $('#disponiblesInput').val('Agotado'); // Indicar agotado
                    } else {
                        actualizarEstadoFormulario(false); // Habilitar campos
                        $('#disponiblesInput').val(response.disponible); // Mostrar stock disponible
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error: ", error);
                    // Limpiar los campos y deshabilitar si hay un error
                    $('#nombreElementoInput').val('');
                    $('#disponiblesInput').val('');
                    $('#cantidadElemento').val('');
                    actualizarEstadoFormulario(true);
                }
            });
        } else {
            // Limpiar y habilitar los campos si el input de ID está vacío
            $('#nombreElementoInput').val('');
            $('#disponiblesInput').val('');
            $('#cantidadElemento').val('');
            actualizarEstadoFormulario(false);
        }
    });
});