import re
s = input()

email = re.search(r"[^\s@]+@[^\s@]+\.[^\s@]+", s)

if email:
    print(email.group(0))
else:
    print("No email")
