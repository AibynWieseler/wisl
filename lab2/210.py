n = int(input())
arr = input().split()

arr.sort(key=int)
arr.reverse()

print(" ".join(arr))