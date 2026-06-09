import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# =====================================================
# CONFIGURACIÓN DE CARPETAS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
DOCS_DIR = BASE_DIR / "docs"
LOGS_DIR = BASE_DIR / "logs"

PROCESSED_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

etl_logs = []


def log(step, status, records=0, message=""):
    etl_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "step": step,
        "status": status,
        "records": records,
        "message": message
    })


def load_json(filename):
    path = RAW_DIR / filename

    if not path.exists():
        path = BASE_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_prop(record, field):
    return record.get("properties", {}).get(field)


def clean_text(value):
    if value is None:
        return None
    value = str(value).strip()
    if value == "":
        return None
    return value


def clean_email(value):
    value = clean_text(value)
    if value is None:
        return None
    return value.lower()


def to_number(value):
    try:
        if value in [None, "", "null"]:
            return 0
        return float(value)
    except:
        return 0


def to_date(value):
    try:
        if value in [None, "", "null"]:
            return None
        return pd.to_datetime(value).date()
    except:
        return None


# =====================================================
# CARGA RAW
# =====================================================

chartmogul_customers = load_json("chartmogul_customers.json")
hubspot_contacts = load_json("hubspot_contacts.json")
hubspot_companies = load_json("hubspot_companies.json")
hubspot_deals = load_json("hubspot_deals_enriched.json")
posthog_events_raw = load_json("posthog_recent_events.json")

log("Load ChartMogul Customers", "OK", len(chartmogul_customers))
log("Load HubSpot Contacts", "OK", len(hubspot_contacts))
log("Load HubSpot Companies", "OK", len(hubspot_companies))
log("Load HubSpot Deals", "OK", len(hubspot_deals))

# =====================================================
# DIM_CLIENTE
# Fuente principal: ChartMogul
# =====================================================

clientes_rows = []

for c in chartmogul_customers:
    mrr = to_number(c.get("mrr"))
    arr = to_number(c.get("arr"))
    status = clean_text(c.get("status"))

    clientes_rows.append({
        "cliente_id_natural": clean_text(c.get("uuid")),
        "chartmogul_id": c.get("id"),
        "external_id": clean_text(c.get("external_id")),
        "email": clean_email(c.get("email")),
        "nombre_cliente": clean_text(c.get("name")),
        "empresa": clean_text(c.get("company")),
        "pais_codigo": clean_text(c.get("country")),
        "estado_cliente": status,
        "lead_status": clean_text(c.get("lead_status")),
        "fecha_cliente_desde": to_date(c.get("customer-since")),
        "mrr": mrr,
        "arr": arr,
        "es_cliente_pago": 1 if mrr > 0 else 0,
        "es_activo": 1 if status == "Active" else 0,
        "es_churn": 1 if status == "Cancelled" else 0,
        "es_past_due": 1 if status == "Past Due" else 0
    })

dim_cliente = pd.DataFrame(clientes_rows)

dim_cliente = dim_cliente.drop_duplicates(
    subset=["cliente_id_natural"]
).reset_index(drop=True)

dim_cliente.insert(0, "sk_cliente", range(1, len(dim_cliente) + 1))

dim_cliente.to_csv(
    PROCESSED_DIR / "dim_cliente.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_cliente", "OK", len(dim_cliente))


# =====================================================
# DIM_PAIS
# =====================================================

dim_pais = dim_cliente[["pais_codigo"]].drop_duplicates()
dim_pais = dim_pais[dim_pais["pais_codigo"].notna()].reset_index(drop=True)
dim_pais.insert(0, "sk_pais", range(1, len(dim_pais) + 1))

dim_pais.to_csv(
    PROCESSED_DIR / "dim_pais.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_pais", "OK", len(dim_pais))


# =====================================================
# DIM_ESTADO_CLIENTE
# =====================================================

dim_estado_cliente = dim_cliente[["estado_cliente"]].drop_duplicates()
dim_estado_cliente = dim_estado_cliente[
    dim_estado_cliente["estado_cliente"].notna()
].reset_index(drop=True)

dim_estado_cliente.insert(
    0,
    "sk_estado_cliente",
    range(1, len(dim_estado_cliente) + 1)
)

dim_estado_cliente.to_csv(
    PROCESSED_DIR / "dim_estado_cliente.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_estado_cliente", "OK", len(dim_estado_cliente))


# =====================================================
# DIM_EMPRESA
# Fuente: HubSpot Companies
# =====================================================

empresa_rows = []

for company in hubspot_companies:
    empresa_rows.append({
        "empresa_id_natural": company.get("id"),
        "nombre_empresa": clean_text(get_prop(company, "name")),
        "dominio": clean_text(get_prop(company, "domain")),
        "fecha_creacion": to_date(get_prop(company, "createdate")),
        "fecha_modificacion": to_date(get_prop(company, "hs_lastmodifieddate"))
    })

dim_empresa = pd.DataFrame(empresa_rows)

dim_empresa = dim_empresa.drop_duplicates(
    subset=["empresa_id_natural"]
).reset_index(drop=True)

dim_empresa.insert(0, "sk_empresa", range(1, len(dim_empresa) + 1))

dim_empresa.to_csv(
    PROCESSED_DIR / "dim_empresa.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_empresa", "OK", len(dim_empresa))


# =====================================================
# DIM_PIPELINE
# Fuente: HubSpot Deals
# =====================================================

pipeline_rows = []

for deal in hubspot_deals:
    pipeline_rows.append({
        "pipeline": clean_text(get_prop(deal, "pipeline")),
        "dealstage": clean_text(get_prop(deal, "dealstage"))
    })

dim_pipeline = pd.DataFrame(pipeline_rows).drop_duplicates().reset_index(drop=True)
dim_pipeline.insert(0, "sk_pipeline", range(1, len(dim_pipeline) + 1))

dim_pipeline.to_csv(
    PROCESSED_DIR / "dim_pipeline.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_pipeline", "OK", len(dim_pipeline))


# =====================================================
# POSTHOG EVENTS
# =====================================================

posthog_results = posthog_events_raw.get("results", [])

event_rows = []

for row in posthog_results:
    if len(row) >= 4:
        event_rows.append({
            "evento": clean_text(row[0]),
            "distinct_id": clean_text(row[1]),
            "fecha_evento": to_date(row[2]),
            "timestamp_evento": row[2],
            "properties": row[3]
        })

df_events = pd.DataFrame(event_rows)

log("Prepare PostHog Events", "OK", len(df_events))


# =====================================================
# DIM_EVENTO
# =====================================================

dim_evento = df_events[["evento"]].drop_duplicates().reset_index(drop=True)
dim_evento.insert(0, "sk_evento", range(1, len(dim_evento) + 1))

dim_evento.to_csv(
    PROCESSED_DIR / "dim_evento.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_evento", "OK", len(dim_evento))


# =====================================================
# DIM_TIEMPO
# Fechas desde ChartMogul, HubSpot y PostHog
# =====================================================

fechas = []

fechas.extend(dim_cliente["fecha_cliente_desde"].dropna().tolist())
fechas.extend(dim_empresa["fecha_creacion"].dropna().tolist())
fechas.extend(df_events["fecha_evento"].dropna().tolist())

for deal in hubspot_deals:
    fechas.append(to_date(get_prop(deal, "createdate")))
    fechas.append(to_date(get_prop(deal, "closedate")))

fechas = list(set([f for f in fechas if f is not None]))

dim_tiempo = pd.DataFrame({"fecha": fechas})
dim_tiempo["fecha"] = pd.to_datetime(dim_tiempo["fecha"])
dim_tiempo = dim_tiempo.sort_values("fecha").reset_index(drop=True)

dim_tiempo["anio"] = dim_tiempo["fecha"].dt.year
dim_tiempo["mes"] = dim_tiempo["fecha"].dt.month
dim_tiempo["nombre_mes"] = dim_tiempo["fecha"].dt.month_name()
dim_tiempo["trimestre"] = dim_tiempo["fecha"].dt.quarter
dim_tiempo["semana"] = dim_tiempo["fecha"].dt.isocalendar().week
dim_tiempo["dia"] = dim_tiempo["fecha"].dt.day
dim_tiempo["anio_mes"] = dim_tiempo["fecha"].dt.strftime("%Y-%m")

dim_tiempo.insert(0, "sk_tiempo", range(1, len(dim_tiempo) + 1))

dim_tiempo.to_csv(
    PROCESSED_DIR / "dim_tiempo.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create dim_tiempo", "OK", len(dim_tiempo))


# =====================================================
# MAPAS DE LLAVES SUBROGADAS
# =====================================================

map_cliente = dict(
    zip(dim_cliente["cliente_id_natural"], dim_cliente["sk_cliente"])
)

map_pais = dict(
    zip(dim_pais["pais_codigo"], dim_pais["sk_pais"])
)

map_estado = dict(
    zip(dim_estado_cliente["estado_cliente"], dim_estado_cliente["sk_estado_cliente"])
)

map_tiempo = dict(
    zip(dim_tiempo["fecha"].dt.date, dim_tiempo["sk_tiempo"])
)

map_pipeline = {
    (row["pipeline"], row["dealstage"]): row["sk_pipeline"]
    for _, row in dim_pipeline.iterrows()
}

map_evento = dict(
    zip(dim_evento["evento"], dim_evento["sk_evento"])
)


# =====================================================
# FACT_RETENCION
# Fuente: ChartMogul
# =====================================================

fact_retention_rows = []

for c in chartmogul_customers:
    uuid = clean_text(c.get("uuid"))
    status = clean_text(c.get("status"))
    country = clean_text(c.get("country"))
    fecha_cliente_desde = to_date(c.get("customer-since"))
    mrr = to_number(c.get("mrr"))
    arr = to_number(c.get("arr"))

    fact_retention_rows.append({
        "sk_cliente": map_cliente.get(uuid),
        "sk_pais": map_pais.get(country),
        "sk_estado_cliente": map_estado.get(status),
        "sk_tiempo_cliente_desde": map_tiempo.get(fecha_cliente_desde),
        "mrr": mrr,
        "arr": arr,
        "cantidad_cliente": 1,
        "flag_cliente_pago": 1 if mrr > 0 else 0,
        "flag_activo": 1 if status == "Active" else 0,
        "flag_cancelado": 1 if status == "Cancelled" else 0,
        "flag_past_due": 1 if status == "Past Due" else 0,
        "riesgo_churn": (
            "Alto" if status == "Past Due"
            else "Churned" if status == "Cancelled"
            else "Bajo" if status == "Active"
            else "No aplica"
        )
    })

fact_retention = pd.DataFrame(fact_retention_rows)

fact_retention.to_csv(
    PROCESSED_DIR / "fact_retention.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create fact_retention", "OK", len(fact_retention))


# =====================================================
# FACT_PIPELINE
# Fuente: HubSpot Deals
# =====================================================

fact_pipeline_rows = []

for deal in hubspot_deals:
    createdate = to_date(get_prop(deal, "createdate"))
    closedate = to_date(get_prop(deal, "closedate"))
    pipeline = clean_text(get_prop(deal, "pipeline"))
    dealstage = clean_text(get_prop(deal, "dealstage"))

    amount = to_number(get_prop(deal, "amount"))

    fact_pipeline_rows.append({
        "deal_id": deal.get("id"),
        "sk_tiempo_creacion": map_tiempo.get(createdate),
        "sk_tiempo_cierre": map_tiempo.get(closedate),
        "sk_pipeline": map_pipeline.get((pipeline, dealstage)),
        "amount": amount,
        "cantidad_deal": 1,
        "dealname": clean_text(get_prop(deal, "dealname")),
        "clasificacion_del_lead": clean_text(get_prop(deal, "clasificacion_del_lead")),
        "canal_de_adquisicion": clean_text(get_prop(deal, "canal_de_adquisicion")),
        "closed_lost_reason": clean_text(get_prop(deal, "closed_lost_reason")),
        "closed_won_reason": clean_text(get_prop(deal, "closed_won_reason")),
        "days_to_close": to_number(get_prop(deal, "days_to_close")),
        "flag_tiene_monto": 1 if amount > 0 else 0
    })

fact_pipeline = pd.DataFrame(fact_pipeline_rows)

fact_pipeline.to_csv(
    PROCESSED_DIR / "fact_pipeline.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create fact_pipeline", "OK", len(fact_pipeline))


# =====================================================
# FACT_PRODUCT_USAGE
# Fuente: PostHog
# =====================================================

if len(df_events) > 0:
    usage_grouped = df_events.groupby(
        ["fecha_evento", "evento", "distinct_id"],
        dropna=False
    ).size().reset_index(name="cantidad_eventos")

    fact_usage_rows = []

    for _, row in usage_grouped.iterrows():
        fecha_evento = row["fecha_evento"]
        evento = row["evento"]

        fact_usage_rows.append({
            "sk_tiempo": map_tiempo.get(fecha_evento),
            "sk_evento": map_evento.get(evento),
            "distinct_id": row["distinct_id"],
            "cantidad_eventos": row["cantidad_eventos"]
        })

    fact_product_usage = pd.DataFrame(fact_usage_rows)

else:
    fact_product_usage = pd.DataFrame(
        columns=[
            "sk_tiempo",
            "sk_evento",
            "distinct_id",
            "cantidad_eventos"
        ]
    )

fact_product_usage.to_csv(
    PROCESSED_DIR / "fact_product_usage.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create fact_product_usage", "OK", len(fact_product_usage))


# =====================================================
# TABLA DE TRANSFORMACIONES
# =====================================================

transformations = [
    {
        "campo_destino": "dim_cliente.email",
        "campo_origen": "ChartMogul.email",
        "regla_aplicada": "Normalización a minúscula y eliminación de espacios",
        "comentarios": "Permite homologar correos"
    },
    {
        "campo_destino": "dim_cliente.es_cliente_pago",
        "campo_origen": "ChartMogul.mrr",
        "regla_aplicada": "Si MRR > 0 entonces 1, si no 0",
        "comentarios": "Clasificación de cliente de pago"
    },
    {
        "campo_destino": "dim_cliente.es_churn",
        "campo_origen": "ChartMogul.status",
        "regla_aplicada": "Si status = Cancelled entonces 1",
        "comentarios": "Identificación de clientes cancelados"
    },
    {
        "campo_destino": "fact_retention.riesgo_churn",
        "campo_origen": "ChartMogul.status",
        "regla_aplicada": "Past Due = Alto, Cancelled = Churned, Active = Bajo",
        "comentarios": "Regla de clasificación de riesgo"
    },
    {
        "campo_destino": "dim_tiempo",
        "campo_origen": "Fechas de HubSpot, ChartMogul y PostHog",
        "regla_aplicada": "Derivación de año, mes, trimestre, semana y año-mes",
        "comentarios": "Dimensión obligatoria del modelo"
    },
    {
        "campo_destino": "llaves subrogadas",
        "campo_origen": "IDs naturales de APIs",
        "regla_aplicada": "Generación secuencial de SK para dimensiones",
        "comentarios": "Requisito dimensional"
    },
    {
        "campo_destino": "fact_pipeline.flag_tiene_monto",
        "campo_origen": "HubSpot.amount",
        "regla_aplicada": "Si amount > 0 entonces 1, si no 0",
        "comentarios": "Validación de deals con monto"
    },
    {
        "campo_destino": "fact_product_usage.cantidad_eventos",
        "campo_origen": "PostHog.events",
        "regla_aplicada": "Agrupación por fecha, evento y usuario",
        "comentarios": "Resumen de actividad del producto"
    }
]

df_transformations = pd.DataFrame(transformations)

df_transformations.to_csv(
    DOCS_DIR / "transformation_mapping.csv",
    index=False,
    encoding="utf-8-sig"
)

log("Create transformation_mapping", "OK", len(df_transformations))


# =====================================================
# BITÁCORA ETL
# =====================================================

df_logs = pd.DataFrame(etl_logs)

df_logs.to_csv(
    LOGS_DIR / "etl_log.csv",
    index=False,
    encoding="utf-8-sig"
)


# =====================================================
# RESUMEN FINAL
# =====================================================

print("\n================================")
print("ETL COMPLETADO")
print("================================")

print("\nArchivos generados en processed:")
for file in PROCESSED_DIR.glob("*.csv"):
    print(file.name)

print("\nArchivos generados en docs:")
for file in DOCS_DIR.glob("transformation_mapping.csv"):
    print(file.name)

print("\nArchivos generados en logs:")
for file in LOGS_DIR.glob("etl_log.csv"):
    print(file.name)

print("\nProceso finalizado correctamente.")
