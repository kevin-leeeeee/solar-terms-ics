import urllib.request
import time

url = f"https://raw.githubusercontent.com/kevin-leeeeee/solar-terms-ics/master/test_crlf.ics?t={int(time.time())}"
with urllib.request.urlopen(url) as response:
    content = response.read()

print(f"URL: {url}")
print(f"First 50 bytes hex: {content[:50].hex(' ')}")
