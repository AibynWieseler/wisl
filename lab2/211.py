first = input().split()
n = int(first[0])
l = int(first[1]) - 1
r = int(first[2]) - 1

arr = input().split()

arr[l:r+1] = arr[l:r+1][::-1]

print(" ".join(arr))