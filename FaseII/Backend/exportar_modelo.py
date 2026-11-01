
from pathlib import Path
import mlflow
import mlflow.sklearn
import skops.io as sio

BASE_DIR = Path(__file__).resolve().parents[2]

mlflow.set_tracking_uri(
    f"sqlite:///{(BASE_DIR / 'mlflow.db').as_posix()}"
)

MODEL_ID = "m-e66f3e9819c5490c9b0074e51041b056"

print("Cargando modelo SVM desde MLflow...")

modelo = mlflow.sklearn.load_model(f"models:/{MODEL_ID}")

destino = BASE_DIR / "FaseII" / "Backend" / "modelo_svm.skops"

sio.dump(modelo, destino)

print("Modelo exportado correctamente:")
print(destino)
