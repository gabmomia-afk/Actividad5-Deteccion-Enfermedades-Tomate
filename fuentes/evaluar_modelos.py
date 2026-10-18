
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)

# ----------------------------------
# CONFIGURACION
# ----------------------------------

BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos"
EVIDENCIAS = BASE / "evidencias"

EVIDENCIAS.mkdir(exist_ok=True)

mlflow.set_tracking_uri(
    "sqlite:///" + (BASE / "mlflow.db").as_posix()
)

MODELOS = {
    "Random_Forest": {
        "id": "m-190cafb1a1a3447781027744396bce32",
        "run_id": "447ceaa6289c475e8b215578e295000a",
    },
    "SVM": {
        "id": "m-e66f3e9819c5490c9b0074e51041b056",
        "run_id": "5c9150263ada494d8c89e1c4d5abc354",
    },
}

# ----------------------------------
# CARGAR DATOS
# ----------------------------------

df = pd.read_csv(DATOS / "test.csv")

columnas_hog = [
    c for c in df.columns if c.startswith("hog_")
]

X_test = df[columnas_hog]
y_test = df["clase"]

resultados = []

# ----------------------------------
# EVALUAR MODELOS
# ----------------------------------

for nombre, info in MODELOS.items():

    print("\nEvaluando:", nombre)

    modelo = mlflow.sklearn.load_model(
        "models:/" + info["id"]
    )

    predicciones = modelo.predict(X_test)

    accuracy = accuracy_score(y_test, predicciones)
    precision = precision_score(
        y_test, predicciones, average="macro",
        zero_division=0
    )
    recall = recall_score(
        y_test, predicciones, average="macro",
        zero_division=0
    )
    f1 = f1_score(
        y_test, predicciones, average="macro",
        zero_division=0
    )

    # ROC-AUC multiclase
    roc_auc = np.nan

    if hasattr(modelo, "predict_proba"):
        probabilidades = modelo.predict_proba(X_test)

        roc_auc = roc_auc_score(
            y_test,
            probabilidades,
            labels=modelo.classes_,
            multi_class="ovr",
            average="macro"
        )

    resultados.append({
        "modelo": nombre,
        "accuracy": accuracy,
        "precision_macro": precision,
        "recall_macro": recall,
        "f1_macro": f1,
        "roc_auc_ovr_macro": roc_auc,
    })

    print(
        classification_report(
            y_test, predicciones,
            zero_division=0
        )
    )

    # Matriz de confusion
    matriz = confusion_matrix(
        y_test,
        predicciones,
        labels=modelo.classes_
    )

    etiquetas = [
        c.replace("Tomato___", "")
        for c in modelo.classes_
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    disp = ConfusionMatrixDisplay(
        confusion_matrix=matriz,
        display_labels=etiquetas
    )

    disp.plot(ax=ax, cmap="Blues", values_format="d")
    ax.set_title("Matriz de confusion - " + nombre)
    plt.xticks(rotation=25)
    plt.tight_layout()

    fig.savefig(
        EVIDENCIAS / f"matriz_{nombre}.png",
        dpi=200
    )
    plt.close(fig)

    # Registrar metricas en el run original
    with mlflow.start_run(run_id=info["run_id"]):
        mlflow.log_metrics({
            "test_accuracy": accuracy,
            "test_precision_macro": precision,
            "test_recall_macro": recall,
            "test_f1_macro": f1,
            "test_roc_auc_ovr_macro": roc_auc,
        })

        mlflow.log_artifact(
            str(EVIDENCIAS / f"matriz_{nombre}.png"),
            artifact_path="evaluacion"
        )

# ----------------------------------
# COMPARACION FINAL
# ----------------------------------

tabla = pd.DataFrame(resultados)

tabla.to_csv(
    EVIDENCIAS / "metricas_finales.csv",
    index=False
)

print("\nRESULTADOS FINALES")
print(tabla.to_string(index=False))

metricas = [
    "accuracy",
    "precision_macro",
    "recall_macro",
    "f1_macro",
    "roc_auc_ovr_macro"
]

ax = tabla.set_index("modelo")[metricas].T.plot(
    kind="bar",
    figsize=(11, 6),
    rot=25
)

ax.set_title("Comparacion de modelos")
ax.set_ylabel("Puntuacion")
ax.set_ylim(0, 1.05)
ax.legend(title="Modelo")

plt.tight_layout()
plt.savefig(
    EVIDENCIAS / "comparacion_final.png",
    dpi=200
)
plt.close()

print("\nEVALUACION FINALIZADA")
print("Evidencias guardadas en:", EVIDENCIAS)
