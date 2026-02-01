n = int(input())
arr = []

for _ in range(n):
    arr.append(input())

first = {}

for i in range(n):
    s = arr[i]
    if s not in first:
        first[s] = i + 1

for s in sorted(first):
    print(s, first[s])  