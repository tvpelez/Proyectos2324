const menuToggle = document.getElementById('menu-toggle');
const barra = document.getElementById('barra');

menuToggle.addEventListener('click', () => {
    barra.classList.toggle('active');
});
