var messageType = "{{ message.tags }}";
var messageText = "{{ message }}";
var confirmButtonText = "Aceptar";

    if (messageType === "success") {
        Swal.fire({
            title: 'Éxito',
            text: messageText,
            icon: 'success',
            confirmButtonText: confirmButtonText
        });
    } else if (messageType === "warning") {
        Swal.fire({
            title: 'Advertencia',
            text: messageText,
            icon: 'warning',
            confirmButtonText: confirmButtonText
        });
    } else if (messageType === "error") {
        Swal.fire({
            title: 'Error',
            text: messageText,
            icon: 'error',
            confirmButtonText: confirmButtonText
        });

    } else if (messageType === "confirm") {
        Swal.fire({
            title: "¿Estás seguro de inhabilitar el elemento?",
            text: "El elemento sera dado de baja",
            icon: "question",
            showCancelButton : true,
            cancelButtonText : "Cancelar",
            confirmButtonText : "Inhabilitar",
            reverseButtons : true,
            confirmButtonColor : "#fc7323",
            iconColor : "#fc7323",
          }).then((result) => {
            if (result.isConfirmed) {
              Swal.fire({
                title: 'Éxito',
                text: messageText,
                icon: 'success',
                confirmButtonText: confirmButtonText
              });
            }
        });

    } else {
        // Otro tipo de mensaje, personalízalo según tus necesidades
        Swal.fire({
            title: 'Mensaje',
            text: messageText,
            icon: 'info',
            confirmButtonText: confirmButtonText
        });
    }