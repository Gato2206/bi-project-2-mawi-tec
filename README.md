# bi-project-2-mawi-tec
BI Project — Business Intelligence TI6900 | Mawi SaaS

---

## Integrantes
- Diego León Abarca – 2022008025
- Dylan Retana Arce – 2018132666
- Gabriel Meza Masís – 2022116316
- Jose Pablo Silesky – 2023135259
- Raquel Gómez Vargas – 20220502

---

## Descripción del Problema

Mawi es una empresa SaaS que utiliza múltiples herramientas para administrar sus operaciones:

- Stripe (pagos y suscripciones)
- HubSpot (gestión comercial)
- ChartMogul (MRR, ARR y churn)
- PostHog (uso del producto)
- Help Scout (soporte al cliente)

Durante el levantamiento de requerimientos se identificaron dos problemas principales:

1. Falta de visibilidad temprana sobre clientes en riesgo de cancelar sus suscripciones.
2. Ausencia de una vista consolidada que permita monitorear el avance hacia las metas de crecimiento definidas para diciembre de 2026.

La información se encuentra distribuida en diferentes sistemas, dificultando el análisis integral del negocio y la toma de decisiones basada en datos.

---

## Objetivo del Proyecto

Diseñar e implementar una solución integral de Inteligencia de Negocios mediante un proceso ETL reproducible y trazable que consolide información de múltiples fuentes operacionales y permita analizar retención, crecimiento, comportamiento del producto y desempeño comercial.

---

## Preguntas de Negocio

1. ¿Cuál es la evolución del MRR y cuántos clientes están en riesgo de cancelar?

2. ¿Cómo se comporta el pipeline comercial y cuál es la tasa de conversión de oportunidades?

3. ¿Qué módulos del producto se utilizan con mayor frecuencia?

4. ¿Qué mercados geográficos generan mayor MRR y presentan mayor churn?

5. ¿Los patrones de uso de la plataforma, como actividad reciente y eventos clave, muestran señales previas al churn,
   y qué tipo de interacción se asocia con clientes que mantienen MRR activo?

---

## Arquitectura de la Solución

La solución implementada sigue la siguiente arquitectura:

Fuentes Operacionales
(Stripe, HubSpot, ChartMogul, PostHog y Help Scout)
↓
Proceso ETL (Python)
↓
Modelo Dimensional (Esquema Estrella)
↓
Power BI
↓
Dashboards Analíticos
↓
Toma de Decisiones

---

### Fuentes de Datos
- ChartMogul
- HubSpot
- PostHog
- Stripe
- Help Scout

---

## Modelo Dimensional

El modelo fue diseñado bajo un esquema estrella compuesto por:

### Tablas de Hechos

- fact_retencion
- fact_pipeline
- fact_uso_producto

### Dimensiones

- dim_cliente
- dim_tiempo
- dim_pais
- dim_estado_cliente
- dim_pipeline
- dim_evento
- dim_empresa

---

## Herramientas Utilizadas

### ETL

- Python
- Pandas
- NumPy

### Almacenamiento

- CSV

### Visualización

- Power BI

### Control de Versiones

- Git
- GitHub

---

## Ejecución del ETL

## Instrucciones de Ejecución

1. Clonar el repositorio.

2. Instalar las dependencias necesarias:

 pip install pandas numpy requests

3. Configurar las credenciales de acceso a las APIs en el archivo .env.

4. Ejecutar el proceso ETL:

   python transform_etl.py

5. Verificar los archivos generados en la carpeta processed.

6. Abrir el archivo Power BI para visualizar los dashboards.

---
## Estructura del Repositorio

Proyecto_Mawi_BI/

├── README.md
├── raw/
├── processed/
├── scripts/
├── docs/
├── logs/
├── transform_etl.py
├── dashboard/
├── informe/
├── presentacion/
└── evidencia/

---

## Principales KPIs

- Total MRR Activo
- Total ARR Activo
- Clientes Activos
- Clientes Churned
- Tasa de Churn
- Clientes Past Due
- MRR Promedio por Cliente
- Total Deals
- Tasa de Conversión
- Tiempo Promedio de Cierre
- Usuarios Activos
- Eventos Totales de Producto

---

## Resultados

La solución permite:

- Monitorear la retención de clientes.
- Identificar riesgos de churn.
- Analizar el desempeño comercial.
- Evaluar el uso de la plataforma.
- Dar seguimiento a indicadores estratégicos del negocio.


