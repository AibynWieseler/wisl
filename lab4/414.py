from datetime import datetime, timezone, timedelta

def parse_datetime(date_str):
    date_part, tz_part = date_str.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    sign = 1 if tz_part[3] == '+' else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])
    offset = timedelta(hours=hours, minutes=minutes) * sign
    tz = timezone(offset)
    return dt.replace(tzinfo=tz)

dt1 = parse_datetime(input()).astimezone(timezone.utc)
dt2 = parse_datetime(input()).astimezone(timezone.utc)

diff_seconds = abs((dt2 - dt1).total_seconds()) #divide for days
diff_days = int(diff_seconds // 86400)
print(diff_days)