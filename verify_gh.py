import requests

url = "https://raw.githubusercontent.com/kevin-leeeeee/solar-terms-ics/master/solar_terms.ics"
resp = requests.get(url)
content = resp.content

print(f"Total length: {len(content)}")
print(f"First 50 bytes hex: {content[:50].hex(' ')}")
print(f"Line endings found: {repr(content[:100])}")
