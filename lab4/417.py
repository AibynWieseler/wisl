import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

a = dx**2 + dy**2
b = 2 * (x1*dx + y1*dy)
c = x1**2 + y1**2 - R**2

disc = b**2 - 4*a*c

if disc < 0: #no intersec
    print(f"{0.0:.10f}")
else:
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)
    
    t_in = max(0, min(t1, t2))
    t_out = min(1, max(t1, t2))
    
    if t_out < t_in:
        length = 0.0
    else:
        segment_length = math.hypot(dx, dy)
        length = (t_out - t_in) * segment_length
    
    print(f"{length:.10f}")