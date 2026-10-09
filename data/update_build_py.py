import re, json

with open('data/build.py', 'r', encoding='utf-8') as f:
    text = f.read()

with open('data/new_hub.json', 'r', encoding='utf-8') as f:
    new_hub = json.load(f)

# Format the dict as a python string
hub_str = "HUB = {\n"
for k, v in sorted(new_hub.items()):
    hub_str += f' "{k}": [{v[0]}, {v[1]}],\n'
hub_str += "}"

# Regex to find the HUB dictionary definition
pattern = re.compile(r'HUB\s*=\s*\{.*?\n\}', re.DOTALL)
new_text = pattern.sub(hub_str, text)

with open('data/build.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated data/build.py with the new HUB coordinates.")
