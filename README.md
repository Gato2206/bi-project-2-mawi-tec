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

## Instrucciones para ejecutar el ETL
1. Preparar el entorno

Instalar Python 3.14 o superior.

Abrir una terminal y ejecutar:

pip install pandas requests
2. Organizar los archivos

Verificar que la estructura del proyecto sea la siguiente:

BI_project
│
├── transform_etl.py
│
├── raw
│   ├── hubspot_contacts.json
│   ├── hubspot_companies.json
│   ├── hubspot_deals_enriched.json
│   ├── chartmogul_customers.json
│   └── posthog_recent_events.json
│
├── processed
├── docs
├── logs
└── scripts

Los archivos JSON dentro de la carpeta raw corresponden a los datos extraídos desde las APIs de HubSpot, ChartMogul y PostHog.

3. Ejecutar el proceso ETL

Ubicarse en la carpeta principal del proyecto y ejecutar:

python transform_etl.py
4. Verificar la ejecución

Si el proceso finaliza correctamente, en la consola aparecerá el mensaje:

ETL COMPLETADO
5. Revisar los resultados

Los archivos generados se almacenarán automáticamente en las siguientes carpetas:

processed/

dim_cliente.csv
dim_empresa.csv
dim_estado_cliente.csv
dim_evento.csv
dim_pais.csv
dim_pipeline.csv
dim_tiempo.csv
fact_pipeline.csv
fact_product_usage.csv
fact_retention.csv

docs/

transformation_mapping.csv

logs/

etl_log.csv
6. Utilizar los datos

Los archivos ubicados en la carpeta processed pueden ser utilizados directamente para construir el modelo dimensional y los dashboards analíticos en Power BI, Tableau u otra herramienta de visualización.
---
## Estructura del Repositorio

Proyecto_Mawi_BI/

├── README.md
│
├── ETL/
│   ├── transform_etl.py
│   ├── extract_chartmogul.py
│   ├── extract_hubspot.py
│   ├── extract_posthog.py
│   ├── config.py
│   └── .env.example
│
├── data/
│   ├── raw/
│   │   ├── chartmogul.json
│   │   ├── hubspot.json
│   │   └── posthog.json
│   │
│   └── processed/
│       ├── dim_cliente.csv
│       ├── dim_tiempo.csv
│       ├── dim_pais.csv
│       ├── dim_estado_cliente.csv
│       ├── dim_pipeline.csv
│       ├── dim_evento.csv
│       ├── dim_empresa.csv
│       ├── fact_retencion.csv
│       ├── fact_pipeline.csv
│       └── fact_uso_producto.csv
│
├── docs/
│   ├── Diccionario_Dimensional.pdf
│   ├── transformation_mapping.xlsx
│   └── logs_etl.txt
│
├── dashboard/
│   └── Mawi.pbix
│
├──Informe_Final.pdf
│
├── MawiPresentacion2026.pdf
│
└── Evidencia de levantamiento de requerimientos

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


