import json
import sys
import os

# Append OSM coords to data/build.py
def process():
    with open('osm_stops.json', 'r', encoding='utf-8') as f:
        osm_data = json.load(f)

    # We need to load canon from build.py
    sys.path.append(os.path.join(os.getcwd(), 'data'))
    from build import canon, stops, HUB
    
    # We will build a list of lines to append or modify
    new_coords = {}
    
    for element in osm_data.get('elements', []):
        tags = element.get('tags', {})
        lat = element.get('lat')
        lon = element.get('lon')
        
        names_to_check = []
        if 'name' in tags:
            names_to_check.append(tags['name'])
        if 'name:en' in tags:
            names_to_check.append(tags['name:en'])
        if 'alt_name' in tags:
            names_to_check.append(tags['alt_name'])
            
        for name in names_to_check:
            # specifically for thana vs ps vs police station
            name_clean = name.replace("Police Station", "PS").replace("Thana", "PS")
            c_name = canon(name_clean)
            if not c_name:
                continue
            
            # Check if it matches an existing stop in the graph
            if c_name in stops and c_name not in HUB and c_name not in new_coords:
                new_coords[c_name] = [round(lat, 6), round(lon, 6)]
                print(f"Matched {c_name} from {name}")

    if not new_coords:
        print("No new stops matched.")
        return

    # Now read build.py to append the new coords to HUB
    with open('data/build.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the HUB dict
    import re
    hub_match = re.search(r'(HUB\s*=\s*\{)(.*?)(\n\})', content, re.DOTALL)
    if hub_match:
        before = content[:hub_match.end(2)]
        after = content[hub_match.end(2):]
        
        append_str = ""
        for name, coords in new_coords.items():
            append_str += f',\n "{name}":{coords}'
            
        new_content = before + append_str + after
        with open('data/build.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added {len(new_coords)} stops to HUB in build.py")

if __name__ == '__main__':
    process()
