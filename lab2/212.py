n = int(input())
arr = input().split()

for i in range(n):
    arr[i] = str(int(arr[i]) ** 2)
print(" ".join(arr))