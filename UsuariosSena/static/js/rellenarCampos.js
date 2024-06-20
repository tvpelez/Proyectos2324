$(document).ready(function () {
    // Cuando se cambia el número de serial
    $(document).ready(function () {
        $('input[name="serialSenaElemento"]').on('input', function () {
            var serialNumber = $(this).val();
            if (serialNumber) {
                $.ajax({
                    url: '/get-element-name-by-serial',
                    type: 'GET',
                    data: { 'serialNumber': serialNumber },
                    success: function (response) {
                        // Actualizar los campos
                        $('input[name="nombreElemento"]').val(response.elementName);
                        $('input[name="valorUnidadElemento"]').val(response.valorUnidad);
                        $('input[name="disponibles"]').val(response.Stock);
                    },
                    error: function (xhr, status, error) {
                        console.error("Error: ", error);
                        // Limpiar los campos si hay un error
                        $('input[name="nombreElemento"]').val('');
                        $('input[name="valorUnidadElemento"]').val('');
                        $('input[name="disponibles"]').val('');
                    }
                });
            } else {
                // Limpiar los campos si el número de serie está vacío
                $('input[name="nombreElemento"]').val('');
                $('input[name="valorUnidadElemento"]').val('');
                $('input[name="disponibles"]').val('');
            }
        });
    });
    //Actualizar campos crear consumible conseleccion ID elemento
    $('#idElementoInput').on('input', function () {
        var elementId = $(this).val();

        if (!elementId) {
            // Limpiar los campos si el input está vacío
            $('#nombreElementoInput').val('');
            $('#disponiblesInput').val('');
            $('#cantidad_prestada').val('');
            $('#observaciones_prestamo').val('');
        } else {
            // Realizar solicitud AJAX si hay un valor
            $.ajax({
                url: '/get_element_consum_info/',
                type: 'GET',
                data: { 'id': elementId },
                success: function (response) {
                    // Actualizar los campos con la respuesta
                    $('#nombreElementoInput').val(response.nombre);
                    $('#disponiblesInput').val(response.disponible);
                },
                error: function (xhr, status, error) {
                    console.error("Error: ", error);
                    // Limpiar los campos si hay un error
                    $('#nombreElementoInput').val('');
                    $('#disponiblesInput').val('');
                    $('#cantidad_prestada').val('');
                    $('#observaciones_prestamo').val('');
                }
            });
        }
    });
});

//AVISO CANCELAR
function confirmCancel() {
    Swal.fire({
        title: '¿Estás seguro que quieres cancelar?',
        text: "Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, volver'
    }).then((result) => {
        if (result.isConfirmed) {
            // Redireccionar al usuario a la página de inicio
            window.location.href = "/elementosdash/";
        }
    });
}