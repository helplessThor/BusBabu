import json

with open('data/raw_dumps/kolbusopedia_new_routes_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

brand_new = data.get('brand_new', [])
updated = data.get('updated', [])

lines = ["var routes_kolbusopedia = ["]
for r in brand_new + updated:
    lines.append(f'"{r} : ",')
lines.append("];")

with open("data/raw_busrepo_routes_kolbusopedia.js", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"Written {len(brand_new) + len(updated)} routes to kolbusopedia js file.")
