n = int(input())
surnames = []

for _ in range(n):
    surname = input()
    surnames.append(surname)

unique_surnames = set(surnames)

print(len(unique_surnames))