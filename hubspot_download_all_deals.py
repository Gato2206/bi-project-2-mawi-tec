import requests
import json


TOKEN = "pat-na1-4ff31cdd-b90a-4d68-9a00-c9a9d98f7176"


BASE_URL = "https://api.hubapi.com/crm/v3/objects/deals"

PROPERTIES = [
    "amount",
    "closedate",
    "createdate",
    "dealname",
    "dealstage",
    "pipeline",
    "hs_lastmodifieddate",
    "hs_object_id",
    "days_to_close",
    "hs_mrr",
    "mrr",
    "hs_arr",
    "descripcion_churn",
    "fecha_churn",
    "razon_churn",
    "customer_id",
    "stripe_customerid",
    "closed_lost_reason",
    "closed_won_reason",
    "canal_de_adquisicion",
    "clasificacion_del_lead",
    "cantidad_de_usuarios",
    "cantidad_de_proyectos"
]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

all_deals = []
after = None

while True:

    params = {
        "limit": 100,
        "properties": ",".join(PROPERTIES)
    }

    if after:
        params["after"] = after

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print("\nERROR")
        print("Status:", response.status_code)
        print(response.text)
        break

    data = response.json()
    deals = data.get("results", [])

    all_deals.extend(deals)

    print(f"Deals descargados: {len(all_deals)}")

    paging = data.get("paging")

    if not paging:
        break

    after = paging["next"]["after"]

print("\n================================")
print("DESCARGA COMPLETADA")
print("================================")
print(f"TOTAL DEALS: {len(all_deals)}")

with open(
    "hubspot_deals_enriched.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_deals,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nArchivo generado:")
print("hubspot_deals_enriched.json")
