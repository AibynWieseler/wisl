n = int(input())
numbers = list(map(int, input().split()))

truth_count = sum(map(bool, numbers))
print(truth_count)