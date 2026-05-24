def fact(num):
    if num == 2:
        return 2

    return num*fact(num-1)

print(fact(4))