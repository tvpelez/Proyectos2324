function mostrarFechaYHora() {
    // Crear una instancia del objeto Date
    const fechaActual = new Date();

    // Obtener la fecha actual
    const dia = fechaActual.getDate();
    const mes = fechaActual.getMonth() + 1; // Los meses en JavaScript comienzan desde 0
    const anio = fechaActual.getFullYear();

    // Obtener la hora actual
    const hora = fechaActual.getHours();
    const minutos = fechaActual.getMinutes();
    const segundos = fechaActual.getSeconds();

    // Obtener el elemento div
    const divFechaHora = document.getElementById("fechaHora");

    // Formatear la fecha y la hora en un formato deseado
    const fechaHoraFormateada = `${dia}/${mes}/${anio} ${hora}:${minutos}:${segundos}`;

    // Actualizar el contenido del div con la fecha y la hora
    divFechaHora.textContent = `${fechaHoraFormateada}`;
}

// Llamar a la función para mostrar la fecha y la hora
mostrarFechaYHora();
