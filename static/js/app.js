
document.addEventListener("DOMContentLoaded", () => {

    // Desaparecer mensajes después de 5 segundos
    const mensajes = document.querySelectorAll(".flash");

    mensajes.forEach((mensaje) => {
        setTimeout(() => {
            mensaje.style.transition = "opacity 0.5s ease";
            mensaje.style.opacity = "0";

            setTimeout(() => {
                mensaje.remove();
            }, 500);
        }, 5000);
    });

    // Evitar envíos repetidos de formularios
    const formularios = document.querySelectorAll("form[data-loading]");

    formularios.forEach((formulario) => {
        formulario.addEventListener("submit", () => {
            const boton = formulario.querySelector('button[type="submit"]');

            if (boton) {
                boton.disabled = true;
                boton.textContent = "Procesando...";
            }
        });
    });

    console.log("BLISS: interfaz inicializada correctamente.");

});
