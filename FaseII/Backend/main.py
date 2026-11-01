from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from io import BytesIO

import cv2
import skops.io as sio
import numpy as np

from PIL import Image, UnidentifiedImageError
from skimage.feature import hog
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(
    title="Vivero Oruga IA",
    description="Sistema de clasificación de enfermedades en hojas de tomate",
    version="1.1.0"
)

BASE_DIR = Path(__file__).resolve().parents[2]

FRONTEND_DIR = BASE_DIR / "FaseII" / "Frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

MODELO_PATH = Path(__file__).resolve().parent / "modelo_svm.skops"

tipos_desconocidos = sio.get_untrusted_types(file=MODELO_PATH)

if tipos_desconocidos:
    raise RuntimeError(
        f"El modelo contiene tipos no autorizados: {tipos_desconocidos}"
    )

modelo = sio.load(MODELO_PATH, trusted=[])
print("Modelo SVM cargado correctamente desde Skops")

CLASES = {
    "Tomato___healthy": "Hoja saludable",
    "Tomato___Early_blight": "Tizón temprano",
    "Tomato___Late_blight": "Tizón tardío"
}


@app.get("/")
def inicio():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def verificar_estado():
    return {
        "status": "ok",
        "modelo_cargado": True
    }


@app.post("/predict")
async def predecir(file: UploadFile = File(...)):

    if file.content_type not in [
        "image/jpeg",
        "image/png"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPG o PNG"
        )

    contenido = await file.read()

    if len(contenido) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="La imagen supera los 10 MB"
        )

    try:
        imagen_pil = Image.open(BytesIO(contenido))
        imagen_pil = imagen_pil.convert("RGB")

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="No se pudo interpretar la imagen"
        )

    imagen = np.array(imagen_pil)

    imagen = cv2.cvtColor(
        imagen,
        cv2.COLOR_RGB2BGR
    )

    imagen = cv2.resize(
        imagen,
        (128, 128)
    )

    gris = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2GRAY
    )

    caracteristicas = hog(
        gris,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        block_norm="L2-Hys"
    )

    entrada = caracteristicas.reshape(1, -1)

    prediccion = modelo.predict(entrada)[0]

    probabilidades = modelo.predict_proba(entrada)[0]

    confianza = float(np.max(probabilidades))

    return {
        "clase": str(prediccion),
        "diagnostico": CLASES.get(
            str(prediccion),
            str(prediccion)
        ),
        "confianza": round(confianza * 100, 2),
        "advertencia": "Resultado orientativo. Requiere validación humana."
    }
