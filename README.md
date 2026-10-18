
# Actividad 5 - Detección de enfermedades en tomate

## 1. Descripción del proyecto

Proyecto de Machine Learning para clasificar imágenes de hojas
de tomate en tres categorías:

- Tomato___healthy: hoja sana
- Tomato___Early_blight: tizón temprano
- Tomato___Late_blight: tizón tardío

Se comparan dos algoritmos supervisados:
Support Vector Machine (SVM) y Random Forest.

## 2. Dataset

Fuente: PlantVillage
Repositorio: https://github.com/spMohanty/PlantVillage-Dataset

Datos originales: 4500 imágenes
Imágenes dañadas: 0
Duplicados exactos eliminados: 14
Imágenes finales: 4486
Resolución: 256 x 256 píxeles

Distribución final:
- Tizón temprano: 1000
- Tizón tardío: 1901
- Hojas sanas: 1585

Las imágenes originales no se incluyen en GitHub
debido a su tamaño.

## 3. Preparación de datos

Se realizaron las siguientes operaciones:

1. Selección de tres categorías de tomate.
2. Validación de integridad de imágenes.
3. Identificación de duplicados exactos.
4. Eliminación de duplicados.
5. Análisis de distribución de clases.
6. Extracción de características HOG.

Cada imagen se representa mediante 1764
características HOG.

El conjunto se dividió en:
- Entrenamiento: 3588 imágenes
- Prueba: 898 imágenes

## 4. Modelos utilizados

### Support Vector Machine (SVM)

Se utilizó un pipeline con StandardScaler y SVC.

Mejores hiperparámetros:
- C: 10
- Kernel: RBF
- Gamma: scale

### Random Forest

Mejores hiperparámetros:
- n_estimators: 200
- max_depth: None
- min_samples_split: 5

Ambos modelos fueron ajustados mediante
GridSearchCV con validación cruzada de 5 folds.

## 5. Resultados

| Métrica | Random Forest | SVM |
|---|---:|---:|
| Accuracy | 0.8430 | 0.8686 |
| Precision macro | 0.8324 | 0.8525 |
| Recall macro | 0.7975 | 0.8357 |
| F1 macro | 0.8046 | 0.8411 |
| ROC-AUC macro | 0.9489 | 0.9653 |

El modelo SVM obtuvo el mejor desempeño general.

La principal dificultad se presentó al identificar
el tizón temprano, donde el SVM obtuvo un recall
aproximado de 0.62.

## 6. Seguimiento con MLflow

Se utilizó MLflow 3.17.1 para registrar:

- Hiperparámetros de los modelos.
- Resultados de validación cruzada.
- Métricas F1-macro.
- Modelos entrenados.
- Ejecuciones de los experimentos.

Experimento:
Actividad5_Deteccion_Enfermedades_Tomate

Backend local:
SQLite (mlflow.db)

## 7. Reproducción del proyecto

Requisitos:
- Python
- Git
- Dependencias de requirements.txt

Crear entorno virtual:

python -m venv .venv

Activar en Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Instalar dependencias:

python -m pip install -r requirements.txt

Obtener el dataset PlantVillage y organizar las
imágenes de las tres categorías seleccionadas
en la estructura esperada por datos_prep.py.

Ejecutar desde la raíz del proyecto:

python fuentes/datos_prep.py
python fuentes/visualizaciones.py
python fuentes/extraer_caracteristicas.py
python fuentes/train.py
python fuentes/entrenar_svm.py
python fuentes/entrenar_rf.py
python fuentes/registrar_mlflow.py
python fuentes/evaluar_modelos.py

Iniciar MLflow:

python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

Abrir en el navegador:
http://127.0.0.1:5000

Nota: antes de ejecutar los scripts debe verificarse
que las rutas del dataset coincidan con las
configuradas en el código.

## 8. Evidencias

La carpeta evidencias contiene:

- Distribución de clases.
- Matrices de confusión.
- Comparación de modelos.
- Métricas finales.
- Resultados de validación cruzada.

## 9. Limitaciones

- Se utilizan únicamente tres categorías.
- Existe desbalance entre las clases.
- Las características HOG no capturan toda la
  información de color y textura.
- Los resultados proceden de PlantVillage y
  requieren validación con imágenes reales
  tomadas fuera del dataset.
- El tizón temprano presenta menor sensibilidad.

## 10. Mejoras futuras

- Evaluar arquitecturas CNN y transfer learning.
- Incorporar imágenes de campo.
- Aplicar técnicas de aumento de datos.
- Mejorar la detección del tizón temprano.
- Automatizar el entrenamiento con MLOps.
- Implementar monitoreo y versionamiento
  formal de datos y modelos.
