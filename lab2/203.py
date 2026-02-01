n = int(input())
numbers = input().split()

total = 0
for i in range(n):
    total += int(numbers[i])

print(total)
