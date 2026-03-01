import re
s = input()

def double_dig(match):
    return match.group(0) * 2

result = re.sub(r'\d', double_dig, s)
print(result)