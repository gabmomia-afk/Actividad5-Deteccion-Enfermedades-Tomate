
# CHANGELOG - Actividad 5

Registro de cambios del proyecto de detección
de enfermedades en hojas de tomate.

## [0.1.0] - 2026-10-18

### Preparación inicial
- Creación de la estructura del proyecto.
- Configuración del entorno virtual de Python.
- Instalación de dependencias.
- Selección del dataset PlantVillage.

### Preparación de datos
- Selección de tres clases de tomate.
- Análisis de 4500 imágenes originales.
- Verificación de imágenes dañadas.
- Detección de 14 duplicados exactos.
- Obtención de 4486 imágenes limpias.
- Generación de análisis estadístico.
- Visualización de distribución de clases.

### Ingeniería de características
- Implementación de extracción HOG.
- Generación de 1764 características por imagen.
- Exportación de características a CSV.

### Entrenamiento
- División estratificada de entrenamiento y prueba.
- Entrenamiento de SVM y Random Forest.
- Ajuste de hiperparámetros mediante GridSearchCV.
- Validación cruzada de cinco particiones.

### Registro de experimentos
- Configuración de MLflow con SQLite.
- Registro de parámetros y métricas.
- Registro de modelos entrenados.
- Comparación de ejecuciones.

### Evaluación
- Evaluación sobre 898 imágenes de prueba.
- Generación de matrices de confusión.
- Cálculo de accuracy, precision, recall y F1.
- Cálculo de ROC-AUC multiclase.
- Comparación gráfica de resultados.

### Resultados
- Accuracy Random Forest: 84.30%.
- Accuracy SVM: 86.86%.
- F1-macro Random Forest: 80.46%.
- F1-macro SVM: 84.11%.
- Selección de SVM como mejor modelo general.

### Control de versiones
- Inicialización del repositorio Git.
- Configuración de la rama main.
- Creación del primer commit.
- Publicación del repositorio privado en GitHub.

### Limitaciones identificadas
- Menor recall para tizón temprano.
- Dataset limitado a condiciones PlantVillage.
- Ausencia de validación con imágenes de campo.
- Necesidad de versionamiento formal del dataset.

### Pendiente
- Incorporar notebook de entrenamiento.
- Integrar capturas de MLflow.
- Elaborar reporte técnico PDF.
- Completar verificación de reproducibilidad.
