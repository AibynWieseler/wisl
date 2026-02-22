from datetime import datetime, timedelta, timezone

def parse_datetime(s):
    date_part, time_part, tz_part = s.split()
    y, m, d = map(int, date_part.split("-"))
    hh, mm, ss = map(int, time_part.split(":"))
    
    sign = 1 if tz_part[3] == '+' else -1 #utc offset
    tz_h = int(tz_part[4:6])
    tz_m = int(tz_part[7:9])
    tz = timezone(sign * timedelta(hours=tz_h, minutes=tz_m))
    
    dt = datetime(y, m, d, hh, mm, ss, tzinfo=tz)
    return dt.astimezone(timezone.utc)

start_str = input().strip()
end_str = input().strip()

start_utc = parse_datetime(start_str)
end_utc = parse_datetime(end_str)

duration = int((end_utc - start_utc).total_seconds())
print(duration)