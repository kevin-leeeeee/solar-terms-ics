from borax.calendars.festivals2 import SolarTerms
from datetime import date

try:
    print(SolarTerms)
    # Try to find all terms in a year
    # Borax might rely on iterating days or a lookup
    # Let's see if there is a helper
    from borax.calendars.lunardate import LunarDate
    
    ls = []
    for m in range(1, 13):
        for d in range(1, 32):
            try:
                ld = LunarDate.from_solar_date(2026, m, d)
                if ld.term:
                    print(f"{2026}-{m}-{d}: {ld.term}")
            except ValueError:
                pass
except Exception as e:
    print(e)
