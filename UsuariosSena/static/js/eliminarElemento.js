document.addEventListener("DOMContentLoaded", function() {
    const botonesEliminar = document.querySelectorAll(".eliminarElemento");
  
    botonesEliminar.forEach(boton => {
      boton.addEventListener("click", function() {
        const registroId = this.getAttribute("data-id");
  
        // Realiza una solicitud al servidor para eliminar el registro utilizando Fetch, Axios u otra biblioteca
        fetch(`/eliminarElemento/${registroId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") // Asegúrate de obtener la cookie CSRF
          }
        })
          .then(response => {
            if (response.status === 200) {
              // Eliminación exitosa
              // Puedes ocultar la fila de la tabla o actualizar la vista
              const filaAEliminar = this.closest("tr");
              filaAEliminar.remove();
            }
          })
          .catch(error => {
            console.error("Error al eliminar el registro", error);
          });
      });
    });
  });
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  