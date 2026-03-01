import re

S = input()
D = input()

part = re.split(D, S)
print(",".join(part))