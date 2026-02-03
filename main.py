import ephem
import math
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event

# 24 Solar Terms (Angle in degrees : Traditional Chinese Name)
# Note: Angles map to 0=Vernal Equinox.
# Order in a year roughly:
# Jan: 小寒(285), 大寒(300)
# Feb: 立春(315), 雨水(330), 驚蟄(345)
# Mar: 春分(0), ...
TERM_ANGLES = {
    0: "春分", 15: "清明", 30: "穀雨", 45: "立夏",
    60: "小滿", 75: "芒種", 90: "夏至", 105: "小暑",
    120: "大暑", 135: "立秋", 150: "處暑", 165: "白露",
    180: "秋分", 195: "寒露", 210: "霜降", 225: "立冬",
    240: "小雪", 255: "大雪", 270: "冬至", 285: "小寒",
    300: "大寒", 315: "立春", 330: "雨水", 345: "驚蟄"
}

def get_ecliptic_lon(jd):
    """Get geocentric ecliptic longitude of the sun at julian date jd."""
    s = ephem.Sun()
    s.compute(jd)
    e = ephem.Ecliptic(s)
    return e.lon # in radians

def find_term_time(start_jd, end_jd, target_degrees):
    """Find exact time when sun longitude equals target_degrees between start_jd and end_jd."""
    target_rad = math.radians(target_degrees)
    
    def condition(jd):
        lon = get_ecliptic_lon(jd)
        diff = lon - target_rad
        # Handle wrap around 0/360
        # If target is 0, nearby could be 359... (6.28 rad)
        # Assuming we are close (within 1 day), jump shouldn't be large except at 0.
        # But here we pass small interval.
        # Let's simple check: normalize to -PI, PI range?
        while diff < -math.pi: diff += 2*math.pi
        while diff > math.pi: diff -= 2*math.pi
        return diff

    # Use ephem's newton not available directly as standalone? 
    # Can use verify simply binary search or scipy.optimize. 
    # Since we don't have scipy, binary search is fine for seconds precision.
    
    low = start_jd
    high = end_jd
    
    term_jd = low
    for _ in range(50): # 50 iterations is plenty for seconds precision
        mid = (low + high) / 2
        val = condition(mid)
        if val > 0: # Sun moved past target
            high = mid
        else:
            low = mid
        term_jd = mid
        
    return term_jd
    
def generate_terms(years):
    terms_found = []
    
    start_date = datetime(min(years), 1, 1)
    end_date = datetime(max(years) + 1, 1, 1) # Until end of last year
    
    current_date = start_date
    
    # We step 1 day at a time
    while current_date < end_date:
        next_date = current_date + timedelta(days=1)
        
        jd_start = ephem.Date(current_date)
        jd_end = ephem.Date(next_date)
        
        lon_start = get_ecliptic_lon(jd_start)
        lon_end = get_ecliptic_lon(jd_end)
        
        # Convert to degrees [0, 360)
        deg_start = math.degrees(lon_start) % 360
        deg_end = math.degrees(lon_end) % 360
        
        # Check if any term angle is typically crossed
        # Simple crossing check:
        # Cross if deg_start <= target < deg_end
        # Or wrap around: deg_start > deg_end (e.g. 359 -> 0.5)
        
        for target in TERM_ANGLES.keys():
            hit = False
            if deg_start <= deg_end:
                if deg_start <= target < deg_end:
                    hit = True
            else: # Wrap around case (360 boundary)
                if target >= deg_start or target < deg_end:
                    hit = True
            
            if hit:
                # Find exact time
                # We need to be careful with Newton method near 0/360 boundary
                # But binary search handles it if we define condition correctly
                # `condition` function needs to avoid wrap issues.
                # Actually, find_term_time uses radians and normalization, should be ok if close.
                
                exact_jd = find_term_time(jd_start, jd_end, target)
                exact_dt = ephem.Date(exact_jd).datetime()
                # ephem.Date gives UTC naive datetime
                terms_found.append((TERM_ANGLES[target], exact_dt))
        
        current_date = next_date

    return terms_found

def create_ics(terms, filename="solar_terms.ics"):
    c = Calendar()
    c.creator = "Antigravity/SolarTermsGen"
    
    tz_tpe = pytz.timezone('Asia/Taipei')
    
    for name, dt_utc in terms:
        # dt_utc is naive, but it is UTC.
        # Make it aware
        dt_aware = pytz.utc.localize(dt_utc)
        
        # Convert to TPE for description (optional), but ICS event should be accurate
        dt_tpe = dt_aware.astimezone(tz_tpe)
        
        e = Event()
        e.name = name
        e.begin = dt_tpe.date() # Use local date for all-day event
        e.make_all_day()
        
        e.description = f"{name} 精確時間: {dt_tpe.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)"
        c.events.add(e)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(c.serialize())

if __name__ == "__main__":
    today = datetime.now()
    # Generate for this year and next 2 years
    years = [today.year, today.year + 1, today.year + 2]
    print(f"Generating Solar Terms for years: {years}")
    
    terms = generate_terms(years)
    # Sort terms by time
    terms.sort(key=lambda x: x[1])
    
    create_ics(terms)
    print(f"Generated solar_terms.ics with {len(terms)} events.")
