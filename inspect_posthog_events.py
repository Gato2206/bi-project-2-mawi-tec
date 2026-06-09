import json
from collections import Counter

with open(
    "posthog_recent_events.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

results = data.get("results", [])

print("\n================================")
print("TOTAL EVENTOS DESCARGADOS")
print("================================")
print(len(results))

event_counter = Counter()

for row in results:
    event_name = row[0]
    event_counter[event_name] += 1

print("\n================================")
print("TOP 30 EVENTOS")
print("================================")

for event, qty in event_counter.most_common(30):
    print(f"{event}: {qty}")

print("\n================================")
print("PRIMER REGISTRO")
print("================================")

if results:
    print(json.dumps(results[0], indent=4, ensure_ascii=False)[:3000])
