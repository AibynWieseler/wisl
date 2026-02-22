def div_3_4(n):
    for i in range(0, n + 1, 12):
        yield i

n = int(input())
for num in div_3_4(n):
    print(num, end=" ")