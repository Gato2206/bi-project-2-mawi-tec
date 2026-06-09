import requests
import json

TOKEN = "phx_Rn7GNHYaFTkNXm3mtLUbaaDPrFz5tkeWQpv2XXU8bdtjZoJA"
PROJECT_ID = 20182

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://app.posthog.com/api/projects/{PROJECT_ID}/query/"

query = {
    "query": {
        "kind": "HogQLQuery",
        "query": """
            SELECT
                event,
                distinct_id,
                timestamp,
                properties
            FROM events
            WHERE timestamp >= now() - INTERVAL 365 DAY
            ORDER BY timestamp DESC
            LIMIT 10000
        """
    }
}

response = requests.post(
    url,
    headers=headers,
    json=query
)

print("STATUS:", response.status_code)

if response.status_code != 200:
    print(response.text)
    raise SystemExit()

data = response.json()

with open(
    "posthog_recent_events.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("\nArchivo generado:")
print("posthog_recent_events.json")

print("\nPrimeros registros:")
print(json.dumps(data, indent=4, ensure_ascii=False)[:3000])
