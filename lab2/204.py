n = int(input())
numbers = input().split()
cnt = 0
for i in range(n):
    if int(numbers[i]) > 0:
        cnt += 1
print(cnt)