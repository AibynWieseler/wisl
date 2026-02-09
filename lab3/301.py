def check_number(n):

    for c in str(n):
        if int(c) % 2 != 0:
            print("Not valid")
            return
    print("Valid")

n = int(input())
check_number(n)
