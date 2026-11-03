# API de Prevención de Fraude - Modelo Dual (ML + LLM)

Descripción del Proyecto

Este repositorio contiene el código fuente, el entorno de contenerización y la integración de la API para un sistema inteligente de detección de fraude transaccional. La solución propone una arquitectura dual diseñada para reducir falsos positivos y acelerar las revisiones manuales del back-office:

Modelo Predictivo (Machine Learning): Un modelo de clasificación (Random Forest) entrenado con el dataset oficial de Kaggle (28 variables continuas PCA, Tiempo y Monto) para calcular la probabilidad de fraude en milisegundos.

Modelo Explicativo (IA Generativa): Un módulo integrado para traducir anomalías transaccionales en reportes de lenguaje natural para los analistas de fraude (simulado en esta fase).

Nota sobre el rendimiento del modelo: Tras las pruebas locales, se comprobó que el modelo es sensible matemáticamente a transacciones anómalas (duplicando la probabilidad de fraude frente a un caso base: 0.059% vs 0.029%). Sin embargo, debido al desbalance natural del dataset (99.8% transacciones legítimas), la predicción directa tiende a la clase mayoritaria. En fases productivas futuras se contempla aplicar técnicas de sobremuestreo sintético (SMOTE) para sensibilizar el umbral de decisión.

Estructura del Repositorio

app.py: Código principal de la API desarrollada con FastAPI.

Dockerfile: Archivo de configuración para empaquetar el proyecto en un contenedor Docker.

requirements.txt: Dependencias y librerías necesarias (FastAPI, scikit-learn, pydantic, etc.).

(Nota: El archivo model.pkl se omite por tamaño, pero es requerido localmente para la ejecución).

Ejecución Local (Docker)

Para correr esta API en un entorno local, asegúrate de tener el archivo model.pkl en la raíz del proyecto y ejecuta:

# Construir la imagen de Docker
docker build -t api-fraude-dual .

# Ejecutar el contenedor en el puerto 8000
docker run -d -p 8000:8000 api-fraude-dual


Resumen del Manual de Despliegue en la Nube

La estrategia de despliegue para producción está orientada a una arquitectura PaaS (Platform as a Service) utilizando Google Cloud Run. Esto permite que el contenedor se ejecute de manera escalable, sin necesidad de administrar servidores y optimizando los costos de infraestructura.

Controles de Seguridad Implementados:

Privacidad de Datos (R-01): Comunicación asegurada mediante TLS 1.2+ y uso de variables transformadas por PCA.

Prevención de Inyecciones (R-04): Validación estricta de las 28 variables de entrada en FastAPI para mitigar riesgos de ataques Prompt Injection hacia el LLM.

Flujo de Despliegue (Google Cloud):

Autenticación: Iniciar sesión en el SDK de Google Cloud (gcloud auth login).

Preparación de Imagen: Etiquetar la imagen local de Docker para el Container Registry de GCP (docker tag api-fraude-dual gcr.io/[PROJECT_ID]/api-fraude).

Carga al Registro: Subir la imagen a la nube (docker push gcr.io/[PROJECT_ID]/api-fraude).

Despliegue Serverless: Lanzar el servicio en Cloud Run garantizando que el tráfico pase por controles autenticados (gcloud run deploy ... --platform managed).
