num_commands = int(input())
commands = [input().split() for _ in range(num_commands)]

g = 0 
n = 0 #local

for cmd, val in commands:
    val = int(val)
    if cmd == "global":
        g += val
    elif cmd == "nonlocal":
        n += val

print(f"{g} {n}")