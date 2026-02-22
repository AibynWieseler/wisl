import math

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

def tangent_points(x, y, R):
    d = math.hypot(x, y)
    angle0 = math.atan2(y, x)
    delta = math.acos(R / d)
    theta1 = angle0 + delta
    theta2 = angle0 - delta
    t1 = (R * math.cos(theta1), R * math.sin(theta1)) #tangent coords
    t2 = (R * math.cos(theta2), R * math.sin(theta2))
    return t1, t2

def arc_length(p1, p2, R):
    angle1 = math.atan2(p1[1], p1[0]) #angle between points
    angle2 = math.atan2(p2[1], p2[0])
    dtheta = abs(angle2 - angle1)
    if dtheta > math.pi: #arc
        dtheta = 2*math.pi - dtheta
    return R * dtheta

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

A = (x1, y1)
B = (x2, y2)

dx, dy = x2 - x1, y2 - y1 #check for straight lines 
t = -(x1*dx + y1*dy) / (dx*dx + dy*dy)
t = max(0, min(1, t))
closest = (x1 + t*dx, y1 + t*dy)
if math.hypot(*closest) >= R: #no intersec
    print(f"{distance(A, B):.10f}")
else: 
    tA = tangent_points(x1, y1, R) #tangent points
    tB = tangent_points(x2, y2, R)
    
    min_len = float('inf')
    for ta in tA:
        for tb in tB:
            total = distance(A, ta) + distance(B, tb) + arc_length(ta, tb, R)
            min_len = min(min_len, total)
    print(f"{min_len:.10f}")