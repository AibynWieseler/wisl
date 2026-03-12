n = int(input())
nums = list(map(int, input().split()))

square = map(lambda x: x ** 2, nums)
print(sum(square))