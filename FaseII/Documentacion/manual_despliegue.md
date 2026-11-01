
# Manual de despliegue — Vivero Oruga IA

## 1. Descripción del proyecto

Sistema de clasificación de enfermedades en hojas de tomate mediante un modelo de aprendizaje automático SVM.

El sistema identifica tres categorías:

- Tomato___Early_blight: tizón temprano.
- Tomato___Late_blight: tizón tardío.
- Tomato___healthy: hoja saludable.

## 2. Tecnologías utilizadas

- Python 3.11
- FastAPI
- Scikit-learn
- Scikit-image
- OpenCV
- Docker
- HTML, CSS y JavaScript

## 3. Requisitos

- Docker Desktop instalado y ejecutándose.
- Puerto 8000 disponible.
- Archivos del proyecto y modelo SVM exportado.

## 4. Construcción de la imagen Docker

Abrir una terminal en la carpeta raíz del repositorio y ejecutar:

```powershell
docker build -t vivero-oruga-ia:v1 -f FaseII/Dockerfile .
```

## 5. Ejecución del contenedor

```powershell
docker run --name vivero-oruga -p 8000:8000 vivero-oruga-ia:v1
```

Si el contenedor ya existe y está detenido:

```powershell
docker start vivero-oruga
```

## 6. Acceso a la aplicación

Abrir en el navegador:

http://localhost:8000

## 7. Verificación del servicio

Consultar:

http://localhost:8000/health

Respuesta esperada:

```json
{
  "status": "ok",
  "modelo_cargado": true
}
```

## 8. Predicción

La API dispone del endpoint:

POST /predict

Recibe una imagen JPG o PNG mediante el campo `file`.

Devuelve la clase predicha, diagnóstico, confianza y advertencia.

## 9. Validación

Se evaluaron 898 imágenes originales del conjunto de prueba.

Resultados:

- Respuestas válidas: 898/898.
- Precisión: 86.86%.
- Predicciones correctas: 780.
- Predicciones incorrectas: 118.

Las pruebas también incluyeron formatos no permitidos, imágenes corruptas y archivos mayores de 10 MB.

## 10. Limitaciones

El sistema proporciona resultados orientativos y no sustituye una evaluación fitosanitaria profesional.

El rendimiento es menor para la identificación de tizón temprano, con una sensibilidad del 62%.
