import re
import glob
import json

# Read all existing routes to create a set for fast lookup
existing_routes = set()
for js_file in glob.glob("data/raw_busrepo_routes*.js"):
    with open(js_file, "r", encoding="utf-8") as f:
        for line in f:
            # Match pattern: "ROUTE:From to To [via: ...]"
            match = re.search(r'"([^"]+? \[[^\]]+\])(?: : [^"]+)?', line)
            if match:
                route_str = match.group(1).strip() # just the route part without image
                # Normalize spaces and lowercase for comparison
                route_str = re.sub(r'\s+', ' ', route_str).lower()
                existing_routes.add(route_str)

with open("kolbusopedia_dump.html", "r", encoding="utf-8") as f:
    html = f.read()

# Strip HTML tags before matching to avoid garbage
def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text)

# The content contains HTML entities, replace them
html_clean = strip_tags(html).replace('&nbsp;', ' ').replace('&amp;', '&')

# Pattern for finding routes in cleaned text
# Example: "S-168: Nagerbazar to Howrah Station [via: Dumdum Station]"
matches = re.finditer(r'([a-zA-Z0-9\-/]+(?:\s*\([^)]+\))?)\s*:\s*([^\[]+)\[via:\s*([^\]]+)\]', html_clean, re.IGNORECASE)

new_routes = set()
total_found = 0
for m in matches:
    total_found += 1
    route_no = m.group(1).strip()
    terminals = m.group(2).strip()
    via = m.group(3).strip()
    
    # Reconstruct route string
    route_str = f"{route_no}:{terminals} [via: {via}]"
    route_str = re.sub(r'\s+', ' ', route_str)
    
    # Check if we already have this exact string or similar
    if route_str.lower() not in existing_routes:
        # Before adding, let's also check if the route_no alone is completely new, or just a spelling variant
        new_routes.add(route_str)

print(f"Total existing routes: {len(existing_routes)}")
print(f"Total routes found in HTML: {total_found}")
print(f"New routes found (mismatching existing exactly): {len(new_routes)}")

# Let's filter out ones where we might have the same route number but slightly different via points
# to see if it's a completely new route vs a minor update.
existing_route_numbers = set()
for r in existing_routes:
    parts = r.split(':')
    if parts:
        existing_route_numbers.add(parts[0].strip().lower())

brand_new_routes = []
updated_routes = []

for nr in new_routes:
    rn = nr.split(':')[0].strip().lower()
    if rn in existing_route_numbers:
        updated_routes.append(nr)
    else:
        brand_new_routes.append(nr)

print(f"Brand new routes (new route numbers): {len(brand_new_routes)}")
print(f"Updated routes (existing number, different text): {len(updated_routes)}")

with open("kolbusopedia_new_routes_list.json", "w", encoding="utf-8") as f:
    json.dump({"brand_new": brand_new_routes, "updated": updated_routes}, f, indent=2)

