n = int(input())
numbers = input().split()

max_value = int(numbers[0])
pos = 1

for i in range(1, n):
    current = int(numbers[i])
    if current > max_value:
        max_value = current
        pos = i + 1 

print(pos)