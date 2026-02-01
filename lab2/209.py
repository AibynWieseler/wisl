n = int(input())
numbers = input().split()

min = int(numbers[0])
max = int(numbers[0])

for i in range(1, n):
    current = int(numbers[i])
    if current < min:
        min = current
    if current > max:
        max = current

for i in range(n):
    if int(numbers[i]) == max:
        numbers[i] = str(min)

print(" ".join(numbers))