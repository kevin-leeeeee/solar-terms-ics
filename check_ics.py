with open('solar_terms.ics', 'rb') as f:
    content = f.read(50)
    print(f"Content (hex): {content.hex()}")
    print(f"Content (repr): {repr(content)}")
