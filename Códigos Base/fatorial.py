def fact(num):
    if num == 0 or num == 1:
        return 1

    return num*fact(num-1)

num = 4

print(f"\nRESULTADO DO FATORIAL DE {num}:", fact(num))