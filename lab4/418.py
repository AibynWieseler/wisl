x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

if y1 + y2 == 0:
    xr = (x1 + x2) / 2 
else: #midpoint for horiz
    xr = x2 - y2 * (x2 - x1) / (y1 + y2)

yr = 0.0

print(f"{xr:.10f} {yr:.10f}")