import requests
import json

API_KEY = "60fb57d2185cea195e49851a857bf903"

BASE_URL = "https://api.chartmogul.com/v1/customers"

all_customers = []

page = 1

while True:

    response = requests.get(
        BASE_URL,
        auth=(API_KEY, ""),
        params={
            "page": page,
            "per_page": 200
        }
    )

    if response.status_code != 200:

        print("ERROR:", response.status_code)
        print(response.text)
        break

    data = response.json()

    customers = data.get("entries", [])

    if len(customers) == 0:
        break

    all_customers.extend(customers)

    print(
        f"Página {page} | "
        f"Clientes acumulados: {len(all_customers)}"
    )

    page += 1

print("\n================================")
print("DESCARGA COMPLETADA")
print("================================")
print(f"TOTAL CLIENTES: {len(all_customers)}")

with open(
    "chartmogul_customers.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_customers,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nArchivo generado:")
print("chartmogul_customers.json")
