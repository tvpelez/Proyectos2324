document.addEventListener("DOMContentLoaded", function () {
    var cantidadInput = document.getElementsByName('cantidadElemento')[0];
    var valorUnidadInput = document.getElementsByName('valor_unidad')[0];
    var valorTotalInput = document.getElementsByName('valorTotalElemento')[0];

    function calcularValorTotal() {
        var cantidad = parseInt(cantidadInput.value) || 0;
        var valorUnidad = parseInt(valorUnidadInput.value) || 0;
        var valorTotal = cantidad * valorUnidad;
        valorTotalInput.value = valorTotal;
    }

    function validarYLimpiarCantidad() {
        var cantidad = parseInt(cantidadInput.value);
        if (cantidad < 1 || isNaN(cantidad)) {
            cantidadInput.value = '1';
        }
        calcularValorTotal();
    }

    function validarYLimpiarValorUnidad() {
        if (!/^\d+$/.test(valorUnidadInput.value)) {
            valorUnidadInput.value = '';
            valorTotalInput.value = ''; // Limpia el valor total si el valor de la unidad no es válido
        } else {
            calcularValorTotal();
        }
    }

    cantidadInput.addEventListener('input', validarYLimpiarCantidad);
    valorUnidadInput.addEventListener('input', validarYLimpiarValorUnidad);

    calcularValorTotal();
});
//Desabilitar campos segun sea la elección de la categoría
document.addEventListener('DOMContentLoaded', function () {
    const categoriaSelect = document.getElementById('categoria');
    const cantidadInput = document.getElementById('cantidadElemento');
    const valorTotalInput = document.getElementById('valorTotalElemento');
    const serialInput = document.getElementById('serialInput'); // Referencia al campo de Número de Serie

    function toggleInputsBasedOnCategory() {
        const isDevolutivo = categoriaSelect.value === 'D';
        const isConsumible = categoriaSelect.value === 'C';

        // Desactivar o activar los inputs
        cantidadInput.disabled = isDevolutivo;
        valorTotalInput.disabled = isDevolutivo;
        serialInput.disabled = isConsumible; // Desactiva el campo de Número de Serie si la categoría es Consumible

        // Cambiar el color de fondo para indicar que el campo está desactivado
        cantidadInput.style.backgroundColor = isDevolutivo ? '#e0e0e0' : '';
        valorTotalInput.style.backgroundColor = isDevolutivo ? '#e0e0e0' : '';
        serialInput.style.backgroundColor = isConsumible ? '#e0e0e0' : ''; // Cambia el color de fondo del campo de Número de Serie

        // Si se desactiva y se deselecciona un campo, establece el valor a algo válido
        if (isDevolutivo) {
            cantidadInput.value = '';
            valorTotalInput.value = '';
        }
        if (isConsumible) {
            serialInput.value = ''; // Limpia el campo de Número de Serie si está desactivado
        }
    }

    // Evento para escuchar cambios en el menú desplegable de categoría
    categoriaSelect.addEventListener('change', toggleInputsBasedOnCategory);

    // Llama a la función al cargar la página por si la categoría ya está seleccionada
    toggleInputsBasedOnCategory();
});