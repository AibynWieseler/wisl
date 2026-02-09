triplet_to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}

digit_to_triplet = {v: k for k, v in triplet_to_digit.items()}


def triplets_to_number(s):
    num = ""
    for i in range(0, len(s), 3):
        num += triplet_to_digit[s[i:i+3]]
    return int(num)


def number_to_triplets(n):
    if n == 0:
        return digit_to_triplet["0"]

    result = ""
    for d in str(abs(n)):
        result += digit_to_triplet[d]
    return result


expr = input().strip()

for op in "+-*":
    if op in expr:
        left, right = expr.split(op)
        break

a = triplets_to_number(left)
b = triplets_to_number(right)

if op == "+":
    res = a + b
elif op == "-":
    res = a - b
else:  # *
    res = a * b

print(number_to_triplets(res))
