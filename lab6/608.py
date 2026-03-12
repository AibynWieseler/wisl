n = int(input())
nums = list(map(int, input().split()))

distinct_sort = sorted(set(nums))
print(*distinct_sort)