import requests
import json

TOKEN = "pat-na1-4ff31cdd-b90a-4d68-9a00-c9a9d98f7176"


BASE_URL = "https://api.hubapi.com/crm/v3/objects/contacts"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

all_contacts = []

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

    data = response.json()

    contacts = data.get("results", [])

    all_contacts.extend(contacts)

    print(f"Descargados: {len(all_contacts)} contactos")

    paging = data.get("paging")

    if not paging:
        break

    after = paging["next"]["after"]

print("\nDESCARGA COMPLETADA")
print(f"Total contactos: {len(all_contacts)}")

with open(
    "hubspot_contacts.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_contacts,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nArchivo guardado:")
print("hubspot_contacts.json")
