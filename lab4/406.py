def fibonacchi(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

first = True
n = int(input())
for num in fibonacchi(n):
    if not first:
        print(",", end="")
    print(num, end="")
    first = False