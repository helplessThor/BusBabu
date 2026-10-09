import urllib.request
import re
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://www.kolbusopedia.com/bus-routes',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')

    with open('kolbusopedia_dump.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Downloaded HTML ({len(html)} bytes).")
except Exception as e:
    print(f"Error: {e}")
