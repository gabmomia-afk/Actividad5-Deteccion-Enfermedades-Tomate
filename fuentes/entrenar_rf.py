
from pathlib import Path
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold
)

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO = BASE_DIR / "datos" / "train.csv"
SALIDA = BASE_DIR / "evidencias" / "resultados_rf.csv"

RANDOM_STATE = 42


def entrenar_random_forest():

    print("ACTIVIDAD 5 - RANDOM FOREST")
    print("--------------------------------")

    df = pd.read_csv(ARCHIVO)

    X = df.drop(columns=["archivo", "clase"])
    y = df["clase"]

    modelo = RandomForestClassifier(
        random_state=RANDOM_STATE,
        n_jobs=1
    )

    parametros = {
        "n_estimators": [100, 200],
        "max_depth": [None, 20],
        "min_samples_split": [2, 5]
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    grid = GridSearchCV(
        estimator=modelo,
        param_grid=parametros,
        cv=cv,
        scoring="f1_macro",
        n_jobs=2,
        verbose=2,
        refit=True
    )

    print("\nIniciando GridSearchCV...")

    grid.fit(X, y)

    print("\nENTRENAMIENTO FINALIZADO")
    print("Mejores parametros:", grid.best_params_)
    print("Mejor F1-macro CV:", grid.best_score_)

    resultados = pd.DataFrame(grid.cv_results_)

    SALIDA.parent.mkdir(exist_ok=True)

    resultados.to_csv(
        SALIDA,
        index=False
    )

    print("\nResultados guardados en:", SALIDA)


if __name__ == "__main__":
    entrenar_random_forest()
