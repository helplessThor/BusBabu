import json
import re

transcript_path = r"C:\Users\Kuntal\.gemini\antigravity-ide\brain\808907b2-411a-468d-bc14-afa80ef135c8\.system_generated\logs\transcript_full.jsonl"

osm_json_str = None
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT':
            content = data.get('content', '')
            if 'version' in content and 'Overpass API' in content:
                print("Found match in USER_INPUT")
                # find the first '{' and the last '}'
                start = content.find('{')
                end = content.rfind('}')
                if start != -1 and end != -1:
                    osm_json_str = content[start:end+1]

if osm_json_str:
    with open('osm_stops.json', 'w', encoding='utf-8') as f:
        f.write(osm_json_str)
    print("Extracted osm_stops.json from transcript.")
else:
    print("Could not find JSON in transcript.")
