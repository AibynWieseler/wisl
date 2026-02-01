n = int(input())
arr = input().split()
for i in range(n):
    arr[i] = int(arr[i])

freq = {} 

for x in arr:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_count = 0
most_freq = arr[0]

for key in freq:
    if freq[key] > max_count:
        max_count = freq[key]
        most_freq = key
    elif freq[key] == max_count and key < most_freq:
        most_freq = key

print(most_freq)