
const input = document.getElementById("imagen");
const vistaPrevia = document.getElementById("vistaPrevia");
const boton = document.getElementById("analizar");
const estado = document.getElementById("estado");
const resultado = document.getElementById("resultado");

let urlPrevia = null;

input.addEventListener("change", () => {
    resultado.hidden = true;
    estado.textContent = "";

    if (urlPrevia) {
        URL.revokeObjectURL(urlPrevia);
        urlPrevia = null;
    }

    const archivo = input.files[0];

    if (!archivo) {
        vistaPrevia.hidden = true;
        vistaPrevia.removeAttribute("src");
        return;
    }

    urlPrevia = URL.createObjectURL(archivo);
    vistaPrevia.src = urlPrevia;
    vistaPrevia.hidden = false;
});

boton.addEventListener("click", async () => {
    const archivo = input.files[0];

    if (!archivo) {
        estado.textContent = "Selecciona una imagen primero.";
        return;
    }

    const datos = new FormData();
    datos.append("file", archivo);

    boton.disabled = true;
    resultado.hidden = true;
    estado.textContent = "Analizando imagen...";

    try {
        const respuesta = await fetch("/predict", {
            method: "POST",
            body: datos
        });

        const datosRespuesta = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                datosRespuesta.detail || "Error en el análisis"
            );
        }

        document.getElementById("diagnostico").textContent =
            "Diagnóstico: " + datosRespuesta.diagnostico;

        document.getElementById("confianza").textContent =
            "Confianza estimada: " +
            datosRespuesta.confianza + "%";

        resultado.hidden = false;
        estado.textContent = "Análisis completado.";

    } catch (error) {
        estado.textContent = "Error: " + error.message;
    } finally {
        boton.disabled = false;
    }
});
