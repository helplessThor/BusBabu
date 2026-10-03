import json

with open("kolbusopedia_new_routes_list.json", "r", encoding="utf-8") as f:
    data = json.load(f)

brand_new = data.get("brand_new", [])

# Format them to match the expected raw file style
# E.g. "ROUTE:Origin to Destination [via: X, Y, Z] : ",
lines = ["var routes_kolbusopedia = ["]
for r in brand_new:
    # They are currently formatted as "ROUTE:Origin to Destination [via: X, Y, Z]"
    # We append ' : ' to match the expected format so build.py regex catches it
    lines.append(f'"{r} : ",')
lines.append("];")

with open("data/raw_busrepo_routes_kolbusopedia.js", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
