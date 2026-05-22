def fact(num):
    if num == 2:
        return 2
    
    print(f"Antes: {num}")
    a =  num*fact(num-1)
    print(f"Depois: {num}")

    return a

print(fact(5))