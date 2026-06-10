import json
from collections import Counter

with open(
    "chartmogul_customers.json",
    "r",
    encoding="utf-8"
) as f:

    customers = json.load(f)

print("\n================================")
print("TOTAL CLIENTES")
print("================================")
print(len(customers))

# ---------------------------------
# STATUS
# ---------------------------------

status_counter = Counter()

for c in customers:

    status = c.get("status")

    if status:
        status_counter[status] += 1

print("\n================================")
print("STATUS")
print("================================")

for k, v in status_counter.items():
    print(f"{k}: {v}")

# ---------------------------------
# MRR
# ---------------------------------

mrr_count = 0

for c in customers:

    mrr = c.get("mrr")

    if mrr not in [None, 0, "0"]:
        mrr_count += 1

print("\n================================")
print("CLIENTES CON MRR")
print("================================")
print(mrr_count)

# ---------------------------------
# ARR
# ---------------------------------

arr_count = 0

for c in customers:

    arr = c.get("arr")

    if arr not in [None, 0, "0"]:
        arr_count += 1

print("\n================================")
print("CLIENTES CON ARR")
print("================================")
print(arr_count)

# ---------------------------------
# PAISES
# ---------------------------------

countries = Counter()

for c in customers:

    country = c.get("country")

    if country:
        countries[country] += 1

print("\n================================")
print("TOP 20 PAISES")
print("================================")

for country, qty in countries.most_common(20):
    print(country, qty)
