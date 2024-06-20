const hambur = document.getElementById("hambur");
const aside = document.getElementById("aside");

hambur.addEventListener("click", () => {
    if (aside.style.display === "flex") {
        aside.style.display = "none"; // Cambiar a "none" si está en "flex"
    } else {
        aside.style.display = "flex"; // Cambiar a "flex" si está en "none" u otro valor
    }
});

const enlaces = document.querySelectorAll('.barra-lateral a');

enlaces.forEach((enlace) => {
    enlace.addEventListener("click", (event) => {
        // Quitar la clase 'active' de todos los enlaces
        enlaces.forEach((e) => {
            e.classList.remove("active");
        });

        // Agregar la clase 'active' solo al enlace clicado
        event.target.classList.add("active");
    });
});

function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');
}
