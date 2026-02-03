import os

filename = 'solar_terms.ics'
with open(filename, 'rb') as f:
    data = f.read(200)

print(f"File size: {os.path.getsize(filename)}")
print("First 200 bytes hex:")
print(' '.join(f'{b:02x}' for b in data))
print("\nFirst 200 bytes repr:")
print(repr(data))
