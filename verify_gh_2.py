import urllib.request

url = "https://raw.githubusercontent.com/kevin-leeeeee/solar-terms-ics/master/solar_terms.ics"
with urllib.request.urlopen(url) as response:
    content = response.read()

print(f"Total length: {len(content)}")
print(f"First 50 bytes hex: {content[:50].hex(' ')}")
print(f"Line endings found: {repr(content[:100])}")
