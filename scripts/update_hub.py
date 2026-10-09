import json
from build import canon, HUB, stop_routes

with open(r'C:\Users\Kuntal\.gemini\antigravity-ide\brain\808907b2-411a-468d-bc14-afa80ef135c8\.user_uploaded\media_1790584894084.json', 'r', encoding='utf-8') as f:
    osm_data = json.load(f)

new_stops = {}
for el in osm_data.get('elements', []):
    if el['type'] == 'node' and 'tags' in el:
        names = []
        if 'name' in el['tags']: names.append(el['tags']['name'])
        if 'name:en' in el['tags']: names.append(el['tags']['name:en'])
        if 'alt_name' in el['tags']: names.append(el['tags']['alt_name'])
        
        lat, lon = el['lat'], el['lon']
        for raw_name in names:
            c = canon(raw_name)
            # Only add to HUB if the stop actually exists in our bus routes graph
            if c and c in stop_routes:
                new_stops[c] = [round(lat, 4), round(lon, 4)]

updated = 0
for k, v in new_stops.items():
    if k not in HUB:
        HUB[k] = v
        updated += 1
    elif HUB[k] == [None, None] or HUB[k] == [None, None]:
        HUB[k] = v
        updated += 1

print(f'Added/Updated {updated} relevant stops from OSM.')
with open('new_hub.json', 'w', encoding='utf-8') as f:
    json.dump(HUB, f, indent=2, ensure_ascii=False)
