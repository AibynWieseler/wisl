n = int(input())
words = input().split()

result = []
for i, w in enumerate(words):
    result.append(f'{i}:{w}')

print(' '.join(result))