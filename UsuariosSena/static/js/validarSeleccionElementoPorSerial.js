function actualizarEstadoFormulario(agotado) {
    var campos = [
        'input[name="nombreElemento"]',
        'input[name="disponibles"]',
        'input[name="valorUnidadElemento"]',
        'input[name="observacionesPrestamo"]',
        'input[type="file"]',
        'button[type="submit"]',
    ];

    campos.forEach(function (selector) {
        $(selector).prop('disabled', agotado);
        $(selector).css('background-color', agotado ? '#e0e0e0' : '');
    });
}

$(document).ready(function () {
    $('input[name="serialSenaElemento"]').on('input', function () {
        var serialNumber = $(this).val();

        if (serialNumber) {
            $.ajax({
                url: '/get-element-name-by-serial',
                type: 'GET',
                data: { 'serialNumber': serialNumber },
                success: function (response) {
                    // Actualizar los campos con la respuesta del servidor
                    $('input[name="nombreElemento"]').val(response.elementName);
                    $('input[name="valorUnidadElemento"]').val(response.valorUnidad);

                    // Verificar si el estado del préstamo es 'ACTIVO' o 'VENCIDO', y también verificar el stock
                    var agotado = response.estadoPrestamo === "ACTIVO" || response.estadoPrestamo === "VENCIDO" || response.Stock <= 0;
                    actualizarEstadoFormulario(agotado); // Habilitar o deshabilitar campos basado en si el elemento está prestado o agotado
                    $('input[name="disponibles"]').val(agotado ? 'AGOTADO' : response.Stock); // Si está prestado o agotado, mostrar 'AGOTADO', si no, mostrar stock disponible
                },
                error: function (xhr, status, error) {
                    console.error("Error: ", error);
                    // Limpiar los campos y deshabilitar si hay un error
                    $('input[name="nombreElemento"]').val('');
                    $('input[name="valorUnidadElemento"]').val('');
                    $('input[name="disponibles"]').val('');
                    actualizarEstadoFormulario(true);
                }
            });
        } else {
            // Limpiar y habilitar los campos si el serial está vacío
            $('input[name="nombreElemento"]').val('');
            $('input[name="valorUnidadElemento"]').val('');
            $('input[name="disponibles"]').val('');
            actualizarEstadoFormulario(false);
        }
    });
});

