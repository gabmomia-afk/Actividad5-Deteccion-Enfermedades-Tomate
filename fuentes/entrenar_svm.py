
from pathlib import Path
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold
)

BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVO = BASE_DIR / "datos" / "train.csv"

RANDOM_STATE = 42

def entrenar_svm():

    print("ACTIVIDAD 5 - ENTRENAMIENTO SVM")
    print("--------------------------------")

    df = pd.read_csv(ARCHIVO)

    X = df.drop(columns=["archivo", "clase"])
    y = df["clase"]

    # Pipeline para evitar fuga de datos
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC())
    ])

    # Hiperparametros
    parametros = {
        "svm__C": [0.1, 1, 10],
        "svm__kernel": ["linear", "rbf"],
        "svm__gamma": ["scale"]
    }

    # Validacion cruzada estratificada
    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    grid = GridSearchCV(
        estimator=pipeline,
        param_grid=parametros,
        cv=cv,
        scoring="f1_macro",
        n_jobs=-1,
        verbose=2,
        refit=True
    )

    print("\nIniciando GridSearchCV...")

    grid.fit(X, y)

    print("\nENTRENAMIENTO FINALIZADO")
    print("Mejores parametros:", grid.best_params_)
    print("Mejor F1-macro CV:", grid.best_score_)

    resultados = pd.DataFrame(grid.cv_results_)

    salida = BASE_DIR / "evidencias" / "resultados_svm.csv"
    resultados.to_csv(salida, index=False)

    print("\nResultados guardados en:", salida)


if __name__ == "__main__":
    entrenar_svm()
