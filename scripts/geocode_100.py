import json
import urllib.request
import urllib.parse
import time
import re
import os

print("Loading current stops...")
with open('public/busdata.json', encoding='utf-8') as f:
    data = json.load(f)

# Sort by route frequency to get the most important ones first
missing = [s['name'] for s in data['stops'] if s['lat'] is None]
targets = missing[:100]

print(f"Targeting the next {len(targets)} missing stops.")

results = []
headers = {
    'User-Agent': 'BusBabuKolkataRouter/1.0 (kuntalpauloriginal@gmail.com)'
}

for i, stop in enumerate(targets, 1):
    query = urllib.parse.quote(f"{stop} Kolkata, West Bengal, India")
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        res_data = urllib.request.urlopen(req, timeout=10).read()
        res_json = json.loads(res_data)
        
        if res_json:
            lat = float(res_json[0]['lat'])
            lon = float(res_json[0]['lon'])
            results.append((stop, round(lat, 4), round(lon, 4)))
            print(f"[{i}/100] Found: {stop} -> {lat}, {lon}")
        else:
            # Fallback to broader search
            query2 = urllib.parse.quote(f"{stop}, West Bengal, India")
            url2 = f"https://nominatim.openstreetmap.org/search?q={query2}&format=json&limit=1"
            time.sleep(1.2) # required delay
            req2 = urllib.request.Request(url2, headers=headers)
            res_data2 = urllib.request.urlopen(req2, timeout=10).read()
            res_json2 = json.loads(res_data2)
            if res_json2:
                lat = float(res_json2[0]['lat'])
                lon = float(res_json2[0]['lon'])
                results.append((stop, round(lat, 4), round(lon, 4)))
                print(f"[{i}/100] Found (Fallback): {stop} -> {lat}, {lon}")
            else:
                print(f"[{i}/100] Not found: {stop}")
                
    except Exception as e:
        print(f"[{i}/100] Error on {stop}: {e}")
        
    # Strict 1.5 second delay to respect OSM rate limits (1 req/sec)
    time.sleep(1.5)

if not results:
    print("No coordinates found.")
    exit()

print(f"Successfully geocoded {len(results)}/{len(targets)} stops.")
print("Updating data/build.py...")

with open('data/build.py', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'(HUB\s*=\s*\{.*?)(\n\})', content, re.DOTALL)
if not match:
    print("Could not find HUB dict in build.py!")
    exit(1)

new_lines = []
chunk = []
for stop, lat, lon in results:
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

print("Rebuilding dataset...")
os.system("python data/build.py")
print("Committing and pushing...")
os.system('git add data/build.py public/busdata.json && git commit -m "Add coordinates for 100 more stops via Nominatim" && git push')
print("All done!")
