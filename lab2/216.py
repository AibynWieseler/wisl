n = int(input())
arr = input().split()

seen = set()

for x in arr:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x)