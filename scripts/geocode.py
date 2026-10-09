import json
import urllib.request
import urllib.parse
import concurrent.futures
import re
import os

print("Loading current stops...")
data = json.load(open('public/busdata.json', encoding='utf-8'))
missing = [s['name'] for s in data['stops'] if s['lat'] is None]

print(f"Found {len(missing)} stops without coordinates.")

def geocode(stop):
    query = urllib.parse.quote(f"{stop} Kolkata")
    url = f"https://photon.komoot.io/api/?q={query}&limit=1"
    try:
        res = json.loads(urllib.request.urlopen(url, timeout=5).read())
        if res['features']:
            coords = res['features'][0]['geometry']['coordinates']
            # Photon returns [lon, lat], HUB needs [lat, lon]
            return stop, round(coords[1], 4), round(coords[0], 4)
    except Exception as e:
        pass
    return stop, None, None

print("Starting geocoding (this will take a minute or two)...")
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # process in batches to show progress
    futures = {executor.submit(geocode, s): s for s in missing}
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        stop, lat, lon = future.result()
        if lat and lon:
            results.append((stop, lat, lon))
        if i % 100 == 0:
            print(f"Processed {i}/{len(missing)}... found {len(results)} valid coordinates so far.")

print(f"Finished. Geocoded {len(results)} new stops.")

if not results:
    print("No new stops geocoded.")
    exit()

print("Updating data/build.py...")
with open('data/build.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of HUB dict
match = re.search(r'(HUB\s*=\s*\{.*?)(\n\})', content, re.DOTALL)
if not match:
    print("Could not find HUB dict in build.py!")
    exit(1)

# Format the new entries
# Group them 3 per line to keep it clean
new_lines = []
chunk = []
for stop, lat, lon in results:
    # escape quotes if any
    safe_stop = stop.replace('"', '\\"')
    chunk.append(f'"{safe_stop}":[{lat},{lon}]')
    if len(chunk) == 3:
        new_lines.append(" " + ",".join(chunk) + ",")
        chunk = []
if chunk:
    new_lines.append(" " + ",".join(chunk) + ",")

new_entries_str = "\n" + "\n".join(new_lines)
new_content = content[:match.end(1)] + "," + new_entries_str + content[match.start(2):]

with open('data/build.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("build.py updated. Running build.py to regenerate busdata.json...")
os.system("python data/build.py")
print("All done!")
