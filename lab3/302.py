def isUsual(n):
    if n <= 0:
        return False
    
    for f in (2, 3, 5):
        while n % f == 0:
            n //= f

    return n == 1

n = int(input())
if isUsual(n):
    print("Yes")
else:    
    print("No")