
from pathlib import Path
import csv
import requests
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE = Path(__file__).resolve().parents[2]
TEST_CSV = BASE / "datos" / "test.csv"
IMAGENES = BASE / "datos" / "datos_limp"
SALIDA = BASE / "evidencias" / "resultados_api_docker.csv"
API = "http://localhost:8000/predict"

# Ajustar estos nombres según la respuesta de la API.
CLASES = {
    "Tomato___Early_blight": "Tizón temprano",
    "Tomato___healthy": "Saludable",
    "Tomato___Late_blight": "Tizón tardío",
}

def main():
    datos = pd.read_csv(TEST_CSV, usecols=["archivo", "clase"])
    resultados = []

    for i, fila in enumerate(datos.itertuples(index=False), start=1):
        ruta = IMAGENES / fila.clase / fila.archivo

        try:
            with ruta.open("rb") as imagen:
                respuesta = requests.post(
                    API,
                    files={"file": (ruta.name, imagen, "image/jpeg")},
                    timeout=30,
                )
            respuesta.raise_for_status()
            contenido = respuesta.json()

            # Verificaremos estos nombres de campos antes
            # de ejecutar las 898 pruebas.
            prediccion = contenido.get("clase")
            confianza = contenido.get("confianza")

            resultados.append({
                "archivo": fila.archivo,
                "clase_real": fila.clase,
                "prediccion": prediccion,
                "confianza": confianza,
                "correcto": fila.clase == prediccion,
                "error": "",
            })

        except (requests.RequestException, ValueError) as exc:
            resultados.append({
                "archivo": fila.archivo,
                "clase_real": fila.clase,
                "prediccion": "",
                "confianza": "",
                "correcto": False,
                "error": str(exc),
            })

        if i % 50 == 0 or i == len(datos):
            print(f"Procesadas: {i}/{len(datos)}")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=resultados[0].keys())
        escritor.writeheader()
        escritor.writerows(resultados)

    validos = [r for r in resultados if not r["error"] and r["prediccion"]]
    print(f"\nResultados guardados en: {SALIDA}")
    print(f"Respuestas válidas: {len(validos)}/{len(datos)}")

    if validos:
        reales = [r["clase_real"] for r in validos]
        predichos = [r["prediccion"] for r in validos]

        print(f"Precisión: {accuracy_score(reales, predichos):.4f}")
        print("\nReporte por clase:")
        print(classification_report(reales, predichos, zero_division=0))
        print("\nMatriz de confusión:")
        print(confusion_matrix(
            reales, predichos, labels=list(CLASES.keys())
            ))

if __name__ == "__main__":
    main()
