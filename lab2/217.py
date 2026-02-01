n = int(input())
numbers = []

for _ in range(n):
    num = int(input())
    numbers.append(num)

freq = {}
for num in numbers:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

cnt = 0
for key in freq:
    if freq[key] == 3:
        cnt += 1
print(cnt)