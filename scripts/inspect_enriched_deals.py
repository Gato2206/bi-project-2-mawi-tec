import json


with open(
    "hubspot_deals_enriched.json",
    "r",
    encoding="utf-8"
) as f:

    deals = json.load(f)

print("\n================================")
print("TOTAL DEALS")
print("================================")
print(len(deals))

campos = [
    "hs_mrr",
    "mrr",
    "hs_arr",
    "fecha_churn",
    "razon_churn",
    "descripcion_churn",
    "customer_id",
    "stripe_customerid",
    "amount",
    "dealstage",
    "pipeline",
    "closed_lost_reason",
    "closed_won_reason",
    "canal_de_adquisicion",
    "clasificacion_del_lead",
    "cantidad_de_usuarios",
    "cantidad_de_proyectos"
]

print("\n================================")
print("ANALISIS DE CAMPOS")
print("================================")

for campo in campos:

    cantidad = 0

    for deal in deals:

        properties = deal.get("properties", {})

        valor = properties.get(campo)

        if valor not in [None, "", "null"]:
            cantidad += 1

    porcentaje = round(
        (cantidad / len(deals)) * 100,
        2
    )

    print(
        f"{campo}: "
        f"{cantidad} registros "
        f"({porcentaje}%)"
    )
