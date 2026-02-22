def power_of_2(n):
    for i in range(n + 1):
        yield 2 ** i

n = int(input())

for value in power_of_2(n):
    print(value, end = " ")