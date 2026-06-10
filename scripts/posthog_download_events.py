import requests
import json


TOKEN = "Aquí va el API key de posthog"


PROJECT_ID = 20182

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://app.posthog.com/api/projects/{PROJECT_ID}/event_definitions/"

response = requests.get(
    url,
    headers=headers
)

print("STATUS:", response.status_code)

if response.status_code != 200:
    print(response.text)
    raise SystemExit()

data = response.json()

with open(
    "posthog_event_definitions.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nArchivo generado:")
print("posthog_event_definitions.json")

print("\nPrimeros eventos encontrados:\n")

for event in data.get("results", [])[:20]:

    print(
        event.get("name")
    )
