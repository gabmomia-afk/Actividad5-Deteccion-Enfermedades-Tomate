
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import hashlib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATOS_INI = BASE_DIR / "datos" / "plantvillage_repo" / "raw" / "color"

CLASES = [
    "Tomato___healthy",
    "Tomato___Early_blight",
    "Tomato___Late_blight"
]

def analizar_dataset():
    registros = []
    hashes = {}
    errores = []

    for clase in CLASES:
        carpeta = DATOS_INI / clase

        if not carpeta.is_dir():
            raise FileNotFoundError(
                f"No existe la carpeta: {carpeta}"
            )

        for archivo in sorted(carpeta.iterdir()):
            if not archivo.is_file():
                continue

            try:
                with Image.open(archivo) as img:
                    img.verify()

                with Image.open(archivo) as img:
                    ancho, alto = img.size

                contenido = archivo.read_bytes()
                hash_img = hashlib.sha256(
                    contenido
                ).hexdigest()

                if hash_img in hashes:
                    duplicado = hashes[hash_img]
                else:
                    duplicado = ""
                    hashes[hash_img] = str(archivo)

                registros.append({
                    "archivo": str(archivo.relative_to(BASE_DIR)),
                    "clase": clase,
                    "ancho": ancho,
                    "alto": alto,
                    "duplicado_de": duplicado
                })

            except (OSError, ValueError,
                    UnidentifiedImageError) as e:
                errores.append({
                    "archivo": str(archivo),
                    "error": str(e)
                })

    df = pd.DataFrame(registros)

    print("\nANALISIS DEL DATASET")
    print("----------------------------")
    print("Imagenes validas:", len(df))
    print("Imagenes dañadas:", len(errores))

    if not df.empty:
        print(
            "Duplicados exactos:",
            (df["duplicado_de"] != "").sum()
        )

        print("\nDistribucion por clase:")
        print(df["clase"].value_counts())

        print("\nDimensiones:")
        print(
            df.groupby(["ancho", "alto"])
            .size()
            .head(10)
        )

    salida = BASE_DIR / "datos" / "analisis_imagenes.csv"
    df.to_csv(salida, index=False)

    if errores:
        pd.DataFrame(errores).to_csv(
            BASE_DIR / "datos" / "errores_imagenes.csv",
            index=False
        )

    print("\nAnalisis guardado en:", salida)


import shutil

def limpiar_dataset():
    archivo_csv = BASE_DIR / "datos" / "analisis_imagenes.csv"
    destino = BASE_DIR / "datos" / "datos_limp"

    df = pd.read_csv(archivo_csv).fillna("")

    # Revisar duplicados entre clases diferentes
    duplicados = df[df["duplicado_de"] != ""]
    conflictos = []

    for _, fila in duplicados.iterrows():
        original = df[df["archivo"] == fila["duplicado_de"]]

        if not original.empty:
            clase_original = original.iloc[0]["clase"]

            if clase_original != fila["clase"]:
                conflictos.append(fila["archivo"])

    if conflictos:
        print("ATENCION: Duplicados entre clases diferentes")
        print(conflictos)
        print("Se requiere revision manual.")
        return

    # Evitar mezclar resultados de ejecuciones anteriores
    if destino.exists():
        shutil.rmtree(destino)

    destino.mkdir(parents=True)

    limpios = df[df["duplicado_de"] == ""]

    for _, fila in limpios.iterrows():
        origen = BASE_DIR / fila["archivo"]
        carpeta_destino = destino / fila["clase"]
        carpeta_destino.mkdir(exist_ok=True)

        shutil.copy2(
            origen,
            carpeta_destino / origen.name
        )

    print("\nLIMPIEZA FINALIZADA")
    print("Imagenes originales:", len(df))
    print("Duplicados eliminados:", len(duplicados))
    print("Imagenes limpias:", len(limpios))

    print("\nDistribucion final:")
    print(limpios["clase"].value_counts())

if __name__ == "__main__":
    analizar_dataset()
    limpiar_dataset()
