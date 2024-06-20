document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = () => {
        const passwordField = document.getElementById("password");
        const passwordIcon = document.querySelector(".toggle-password i");

        if (passwordField.type === "password") {
            passwordField.type = "text";
            passwordIcon.classList.replace("fa-eye", "fa-eye-slash");
        } else {
            passwordField.type = "password";
            passwordIcon.classList.replace("fa-eye-slash", "fa-eye");
        }
    };

    const togglePasswordBtn = document.querySelector(".toggle-password");
    togglePasswordBtn.addEventListener("click", togglePassword);
});