n = int(input())
keys = input().split()
values = input().split()

d = dict(zip(keys, values))

query = input()

if query in d:
    print(d[query])
else:
    print("Not found")