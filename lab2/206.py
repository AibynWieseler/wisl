n = int(input())
numbers = input().split()

max = int(numbers[0])
for i in range(n):
    if int(numbers[i]) > max:
        max = int(numbers[i])
print(max)