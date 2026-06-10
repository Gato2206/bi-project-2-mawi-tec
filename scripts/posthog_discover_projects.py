import requests
import json



TOKEN = "Aquí va el API key de posthog"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(
    "https://app.posthog.com/api/projects/",
    headers=headers
)

print("STATUS:", response.status_code)

try:

    data = response.json()

    print("\n================================")
    print("RESPUESTA")
    print("================================")

    print(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        )[:5000]
    )

except Exception as e:

    print("ERROR:")
    print(e)
