
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

DATOS = BASE_DIR / "datos" / "datos_limp"
EVIDENCIAS = BASE_DIR / "evidencias"

EVIDENCIAS.mkdir(exist_ok=True)

clases = {
    "Tomato___healthy": "Tomate sano",
    "Tomato___Early_blight": "Tizón temprano",
    "Tomato___Late_blight": "Tizón tardío"
}

registros = []

for carpeta, nombre in clases.items():
    archivos = list((DATOS / carpeta).glob("*"))

    registros.append({
        "Clase": nombre,
        "Imagenes": len(archivos)
    })

df = pd.DataFrame(registros)

plt.figure(figsize=(9, 5))

barras = plt.bar(
    df["Clase"],
    df["Imagenes"],
    color=["#43A047", "#FB8C00", "#E53935"]
)

plt.title(
    "Distribución de imágenes - PlantVillage",
    fontsize=14
)

plt.xlabel("Categoría")
plt.ylabel("Cantidad de imágenes")

for barra in barras:
    altura = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 15,
        str(int(altura)),
        ha="center"
    )

plt.ylim(0, df["Imagenes"].max() * 1.15)
plt.tight_layout()

plt.savefig(
    EVIDENCIAS / "distribucion_clases.png",
    dpi=300
)

plt.show()

print("\nDistribución del dataset:")
print(df)

print("\nGráfica guardada correctamente.")
