import json

with open('data/raw_dumps/kolbusopedia_new_routes_list.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Keys: {list(d.keys())}")
print(f"Brand new: {len(d.get('brand_new', []))}")
print(f"Updated: {len(d.get('updated', []))}")
if d.get('updated'):
    print("Sample updated route:", d.get('updated')[0])
