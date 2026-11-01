
# Reporte de validación y pruebas
## Vivero Oruga IA — Fase II

### 1. Objetivo

Validar el funcionamiento del sistema de clasificación de enfermedades en hojas de tomate, desplegado mediante Docker y conectado a una interfaz web a través de una API REST desarrollada con FastAPI.

### 2. Entorno de pruebas

- Lenguaje: Python 3.11.
- Modelo: Support Vector Machine (SVM).
- Backend: FastAPI.
- Frontend: HTML, CSS y JavaScript.
- Despliegue: Docker.
- Endpoint de predicción: POST /predict.
- Endpoint de verificación: GET /health.

### 3. Pruebas funcionales

| Prueba | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|
| Verificación de salud | HTTP 200 | HTTP 200 | Aprobada |
| Imagen JPG válida | HTTP 200 y diagnóstico | HTTP 200 y diagnóstico | Aprobada |
| Archivo de texto | HTTP 400 | HTTP 400 | Aprobada |
| Imagen corrupta | HTTP 400 | HTTP 400 | Aprobada |
| Archivo mayor de 10 MB | HTTP 413 | HTTP 413 | Aprobada |

### 4. Evaluación del modelo

Se utilizaron las 898 imágenes originales del conjunto de prueba de la Fase I.

Resultados generales:

- Solicitudes procesadas correctamente: 898 de 898.
- Precisión global: 86.86%.
- Predicciones correctas: 780.
- Predicciones incorrectas: 118.
- F1-score macro: aproximadamente 0.84.

### 5. Resultados por clase

| Clase | Imágenes | Aciertos | Recall |
|---|---:|---:|---:|
| Tizón temprano | 200 | 124 | 62% |
| Hoja saludable | 317 | 312 | 98% |
| Tizón tardío | 381 | 344 | 90% |

### 6. Matriz de confusión

Filas: clase real.
Columnas: clase predicha.

| Clase real / Predicción | Tizón temprano | Saludable | Tizón tardío |
|---|---:|---:|---:|
| Tizón temprano | 124 | 15 | 61 |
| Saludable | 5 | 312 | 0 |
| Tizón tardío | 33 | 4 | 344 |

### 7. Análisis de resultados

El modelo desplegado en Docker alcanzó una precisión de 86.86%, coincidente con la precisión obtenida durante la evaluación de la Fase I.

La categoría saludable presentó el mejor rendimiento, con una sensibilidad aproximada del 98%.

La principal dificultad se identificó en la clasificación del tizón temprano, con una sensibilidad del 62%. En particular, 61 imágenes de tizón temprano fueron clasificadas como tizón tardío.

Este comportamiento sugiere que las características visuales extraídas mediante HOG no siempre permiten distinguir claramente ambas enfermedades.

### 8. Pruebas de casos extremos

El backend rechazó correctamente archivos de texto, imágenes corruptas y archivos superiores al límite de 10 MB.

Estas pruebas demuestran el funcionamiento de las validaciones de formato, integridad y tamaño implementadas en la API.

### 9. Evidencias

- evidencias/docker_contenedor_funcionando.png
- evidencias/validacion_898_docker.png
- evidencias/resultados_api_docker.csv
- evidencias/matriz_SVM.png

### 10. Conclusiones

La Fase II demuestra que el modelo SVM puede ejecutarse dentro de un contenedor Docker y ofrecer predicciones mediante una aplicación web integrada con FastAPI.

Las 898 solicitudes del conjunto de prueba se procesaron correctamente y se obtuvo una precisión del 86.86%.

El sistema es funcional como herramienta orientativa para identificar enfermedades en hojas de tomate, aunque requiere validación humana y futuras mejoras para distinguir con mayor precisión el tizón temprano.
