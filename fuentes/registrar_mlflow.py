
from pathlib import Path
import json

import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

BASE_DIR = Path(__file__).resolve().parent.parent
DATOS = BASE_DIR / "datos" / "train.csv"
MODELOS = BASE_DIR / "modelos"

MODELOS.mkdir(exist_ok=True)

# Base de datos SQLite para registrar experimentos
DB_PATH = BASE_DIR / "mlflow.db"

mlflow.set_tracking_uri(
    DB_PATH.as_uri().replace("file:///", "sqlite:///")
)

mlflow.set_experiment(
    "Actividad5_Deteccion_Enfermedades_Tomate"
)

df = pd.read_csv(DATOS)

X = df.drop(columns=["archivo", "clase"])
y = df["clase"]

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

modelos = {
    "SVM": Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(
            C=10,
            kernel="rbf",
            gamma="scale",
            probability=True
        ))
    ]),
    "Random_Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=5,
        random_state=42,
        n_jobs=1
    )
}

for nombre, modelo in modelos.items():

    print(f"\nRegistrando modelo: {nombre}")

    with mlflow.start_run(run_name=nombre):

        mlflow.log_param("modelo", nombre)
        mlflow.log_param("dataset", "PlantVillage")
        mlflow.log_param("caracteristicas", "HOG")
        mlflow.log_param("random_state", 42)
        mlflow.log_param("cv_folds", 5)

        parametros = modelo.get_params()

        for clave, valor in parametros.items():
            if "__" not in clave:
                mlflow.log_param(
                    clave,
                    str(valor)
                )

        resultados = cross_val_score(
            modelo,
            X,
            y,
            cv=cv,
            scoring="f1_macro",
            n_jobs=1
        )

        mlflow.log_metric(
            "f1_macro_cv",
            float(resultados.mean())
        )

        mlflow.log_metric(
            "f1_macro_std",
            float(resultados.std())
        )

        modelo.fit(X, y)

        if nombre == "Random_Forest": 
            mlflow.sklearn.log_model(
                sk_model=modelo,
                name="modelo",
                skops_trusted_types=[
                    "sklearn.tree._tree.Tree"
                    ]
                    )
        else:
            mlflow.sklearn.log_model(
                sk_model=modelo,
                name="modelo")

        print(
            "F1-macro promedio:",
            resultados.mean()
        )

        print(
            "Desviacion estandar:",
            resultados.std()
        )

print("\nEXPERIMENTOS REGISTRADOS EN MLFLOW")
