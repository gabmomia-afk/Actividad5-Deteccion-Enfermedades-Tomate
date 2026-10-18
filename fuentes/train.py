
from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO = BASE_DIR / "datos" / "caracteristicas.csv"
SALIDA = BASE_DIR / "datos"

RANDOM_STATE = 42

def preparar_entrenamiento():
    print("ACTIVIDAD 5 - PREPARACION DEL ENTRENAMIENTO")
    print("------------------------------------------")

    df = pd.read_csv(ARCHIVO)

    X = df.drop(columns=["archivo", "clase"])
    y = df["clase"]

    print("Total de muestras:", len(df))
    print("Total de caracteristicas:", X.shape[1])

    # Separacion estratificada 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # Conservar identificadores para trazabilidad
    train_df = df.loc[X_train.index].copy()
    test_df = df.loc[X_test.index].copy()

    train_df.to_csv(
        SALIDA / "train.csv",
        index=False
    )

    test_df.to_csv(
        SALIDA / "test.csv",
        index=False
    )

    print("\nDIVISION DEL DATASET")
    print("Entrenamiento:", len(X_train))
    print("Prueba:", len(X_test))

    print("\nDistribucion de entrenamiento:")
    print(y_train.value_counts())

    print("\nDistribucion de prueba:")
    print(y_test.value_counts())

    print("\nArchivos generados:")
    print("datos/train.csv")
    print("datos/test.csv")


if __name__ == "__main__":
    preparar_entrenamiento()
