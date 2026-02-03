import urllib.request
import time

url = f"https://raw.githubusercontent.com/kevin-leeeeee/solar-terms-ics/master/solar_terms.ics?t={int(time.time())}"
with urllib.request.urlopen(url) as response:
    content = response.read()

print(f"URL: {url}")
print(f"Total length: {len(content)}")
print(f"First 50 bytes hex: {content[:50].hex(' ')}")
print(f"Line endings found: {repr(content[:100])}")
