import re

s = input()

up_letters = re.findall(r"[A-Z]", s)
print(len(up_letters))