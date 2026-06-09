import requests
import json



TOKEN = "pat-na1-4ff31cdd-b90a-4d68-9a00-c9a9d98f7176"


BASE_URL = "https://api.hubapi.com/crm/v3/objects/companies"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

all_companies = []

after = None

while True:

    params = {
        "limit": 100
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

    companies = data.get("results", [])

    all_companies.extend(companies)

    print(f"Empresas descargadas: {len(all_companies)}")

    paging = data.get("paging")

    if not paging:
        break

    after = paging["next"]["after"]

print("\n================================")
print("DESCARGA COMPLETADA")
print("================================")
print(f"TOTAL EMPRESAS: {len(all_companies)}")

with open(
    "hubspot_companies.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_companies,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nArchivo generado:")
print("hubspot_companies.json")
