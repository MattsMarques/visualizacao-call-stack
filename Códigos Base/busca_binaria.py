import array

vetor = array.array("i", [0]*6)

vetor[0] = 1
vetor[1] = 3
vetor[2] = 4
vetor[3] = 6
vetor[4] = 9
vetor[5] = 13


print(vetor)

def busca_binaria(vetor, numero, fim, inicio):
    meio = (inicio+fim)//2
    
    if vetor[meio]==numero:
        return meio
        
    elif vetor[meio] < numero:
        return busca_binaria(vetor, numero, fim, meio+1)
        
    elif vetor[meio] > numero:
        return busca_binaria(vetor, numero, meio-1, inicio)    
        
    elif inicio > fim:
        return -1
        

print(busca_binaria(vetor, 9, 6, 0))
        

        
    