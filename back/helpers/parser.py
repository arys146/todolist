from datetime import date, timedelta

def parse_string(string: str): 
    if not string and string == "":
        return None
    string = string.strip()
    parts = string.split(",")
    if len(parts) < 2:
        return None
    t = int(parts[0])
    interval = int(parts[1])
    values = []
    for p in parts[2:]:
        values.append(int(p))
    return t, interval, values

def week_interval(a:date, b:date):
    a_monday = a - timedelta(days=a.weekday())
    b_monday = b - timedelta(days=b.weekday())
    return (b_monday - a_monday).days // 7

def month_interval(a: date, b: date):
    return (b.year - a.year) * 12 + (b.month - a.month)

def is_today(t:int, interval:int, values:int, current:date, start:date):
    if t == 0:
        if (current.weekday() + 1) not in values:
            return False
        if interval == 1:
            return True
        return week_interval(start, current) % interval == 0
    if t == 1:
        if current.day not in values:
            return False
        if interval == 1:
            return True
        return month_interval(start, current) % interval == 0
    return False
    
