
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
from skimage.feature import hog

BASE_DIR = Path(__file__).resolve().parent.parent
DATOS = BASE_DIR / "datos" / "datos_limp"
SALIDA = BASE_DIR / "datos" / "caracteristicas.csv"

CLASES = [
    "Tomato___healthy",
    "Tomato___Early_blight",
    "Tomato___Late_blight"
]

def extraer_caracteristicas():
    registros = []
    total = 0

    for clase in CLASES:
        carpeta = DATOS / clase

        archivos = sorted(
            p for p in carpeta.iterdir()
            if p.is_file()
        )

        print(f"\nProcesando {clase}: {len(archivos)} imágenes")

        for archivo in archivos:
            imagen = cv2.imread(str(archivo))

            if imagen is None:
                raise ValueError(
                    f"No se pudo leer: {archivo}"
                )

            imagen = cv2.resize(imagen, (128, 128))

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

            registro = {
                "archivo": archivo.name,
                "clase": clase
            }

            for i, valor in enumerate(caracteristicas):
                registro[f"hog_{i}"] = float(valor)

            registros.append(registro)
            total += 1

        print(f"Completado: {clase}")

    df = pd.DataFrame(registros)
    df.to_csv(SALIDA, index=False)

    print("\nEXTRACCION FINALIZADA")
    print("Imagenes procesadas:", total)
    print("Caracteristicas HOG:", len(df.columns) - 2)
    print("Archivo generado:", SALIDA)


if __name__ == "__main__":
    extraer_caracteristicas()
