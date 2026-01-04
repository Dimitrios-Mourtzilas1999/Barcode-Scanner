
document.addEventListener('DOMContentLoaded',()=>{
const toggleBtn = document.querySelector(".toggle-password");
    const passwordInput = document.getElementById("password");
    const icon = toggleBtn.querySelector("i");

    toggleBtn.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            icon.classList.replace("fa-eye", "fa-eye-slash");
        } else {
            passwordInput.type = "password";
            icon.classList.replace("fa-eye-slash", "fa-eye");
        }
    });

});